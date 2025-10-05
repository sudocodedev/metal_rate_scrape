from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup as bs

from src.helpers import compute_percent, ist_now, parse_date, parse_float, user_agent
from src.settings import LIVE_RATE_URL
from src.utils import Metal, MetalRate, logger


class LiveRateScrapper:
    name = "live_rate"
    url = LIVE_RATE_URL

    def fetch_content(self):
        response = requests.get(url=self.url, headers={"User-Agent": user_agent()})
        response.raise_for_status()
        return bs(response.content, "html.parser")

    def scrape(self) -> dict:
        content = self.fetch_content()
        GOLD_SELECTOR = "table.table.table-bordered.table-striped.gold-rates tbody tr"
        SILVER_SELECTOR = "table.table.table-bordered.table-striped.silver-rates tbody tr"

        with ThreadPoolExecutor() as executor:
            gold_future = executor.submit(self.parse_table, content, GOLD_SELECTOR, self.parse_gold)
            silver_future = executor.submit(self.parse_table, content, SILVER_SELECTOR, self.parse_silver)
            gold_rates = gold_future.result()
            silver_rates = silver_future.result()

        # forming layout structure
        items = []
        for gold_rate, silver_rate in zip(gold_rates, silver_rates):
            if gold_rate[0] != silver_rate[0]:
                continue

            gold_24k = Metal(date=gold_rate[0], type="gold", purity="24k", price_per_g=gold_rate[1], source=self.name)
            gold_22k = Metal(date=gold_rate[0], type="gold", purity="22k", price_per_g=gold_rate[2], source=self.name)
            silver = Metal(date=silver_rate[0], type="silver", purity=None, price_per_g=silver_rate[1], source=self.name)
            items.append({"rates": [gold_24k, gold_22k, silver]})

        # computing diff and percent
        for i, current_item in enumerate(items[:-1]):
            current_rates, next_rates = current_item["rates"], items[i + 1]["rates"]
            for idx, rate in enumerate(current_rates):
                rate.diff = rate.price_per_g - next_rates[idx].price_per_g
                rate.percent = compute_percent(rate.price_per_g, next_rates[idx].price_per_g)
        if items:
            items.pop()

        timings = self.fetch_timings(content)

        return MetalRate(scraped_at=ist_now(), source=self.name, items=items, last_updated=timings).model_dump(mode="json")

    def parse_table(self, content, selector: str, parse_fn) -> list:
        results = []
        for item in content.select(selector=selector):
            try:
                results.append(parse_fn(item))
            except Exception as e:
                logger.error(f"Exception during gold parsing - {type(e).__name__}: {str(e)}")
        return results

    def parse_gold(self, item):
        data = [data.get_text(strip=True) for data in item.select(selector="td")]
        date_str, *rates_str = data
        date = parse_date(date_str)
        rate_24k_1g, _, rate_22k_1g, _ = map(parse_float, rates_str)
        return [date, rate_24k_1g, rate_22k_1g]

    def parse_silver(self, item):
        data = [data.get_text(strip=True) for data in item.select(selector="td")]
        date_str, *rates_str = data
        date = parse_date(date_str)
        rate_1g, _ = map(parse_float, rates_str)
        return [date, rate_1g]


    def fetch_timings(self, content) -> dict:
        timings = {}
        PREFIX = "Last Update Time: "
        selectors = {
            "gold": "div.col-lg-6.col-md-6.col-xs-12.cgr-usection h5",
            "silver": "div.col-lg-6.col-md-6.col-xs-12.csr-usection h5"
        }

        for metal, selector in selectors.items():
            element = content.select_one(selector)
            if not element:
                continue
            text = element.get_text(strip=True)
            if text.startswith(PREFIX):
                timings[metal] = text.replace(PREFIX, "").strip()
            else:
                timings[metal] = None
        return timings
