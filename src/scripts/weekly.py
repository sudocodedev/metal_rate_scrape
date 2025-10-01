from datetime import datetime, timezone

from src.agent import GeminiInsightAgenticCall, get_insight
from src.db import MongoCollection, get_table
from src.helpers import get_start_end_week_dates
from src.settings import SCRAPER
from src.utils import logger


def get_weekly_rates(collection):
    start_dt, end_dt = get_start_end_week_dates()
    gold_rates = collection.find_many(
        query={
            "date": {"$gte": start_dt, "$lte": end_dt},
            "type": "gold",
            "source": SCRAPER
        },
        ignore_defaults=True
    )
    silver_rates = collection.find_many(
        query={
            "date": {"$gte": start_dt, "$lte": end_dt},
            "type": "silver",
            "source": SCRAPER
        },
        ignore_defaults=True
    )
    return {
        "gold": gold_rates,
        "silver": silver_rates
    }

def main():
    try:
        # collection Initialization
        metal_rate_collection = get_table(name="metal_rate", collection_class=MongoCollection)
        insight_collection = get_table(name="insight", collection_class=MongoCollection)

        # Rates query
        data = get_weekly_rates(collection=metal_rate_collection)

        # Insight generation
        weekly_insight = get_insight(type="weekly", agent=GeminiInsightAgenticCall(), data=data) or ""
        insight_collection.insert_one({
            "status": "success",
            "message": weekly_insight,
            "type": "weekly",
            "sent_at": datetime.now(timezone.utc)
        })
    except Exception as e:
        logger.error(f"{type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    main()
