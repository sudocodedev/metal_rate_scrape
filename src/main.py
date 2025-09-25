# from src.utils import LiveRateScrapper, run_scrapper
# from src.agent import GeminiInsightAgenticCall, get_insight


# def main():
#     data = run_scrapper(scrapper=LiveRateScrapper())
#     print(data)
#     insight = get_insight(type="daily", agent=GeminiInsightAgenticCall(), data=data)
#     print("done...")
#     print(insight)

# if __name__ == "__main__":
#     main()

from src.utils import logger

logger.debug("hi")
logger.info("hi info")
logger.error("hi error")
logger.warning("hi warning")
logger.critical("hi critical")
