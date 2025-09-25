from typing import Protocol


class Scrapper(Protocol):
    name: str = None
    url: str = None

    def scrape(self) -> dict:
        raise NotImplementedError


def run_scrapper(scrapper: Scrapper) -> dict:
    return scrapper.scrape()
