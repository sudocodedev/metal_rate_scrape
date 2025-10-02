from datetime import datetime, timezone

from src.agent import GeminiInsightAgenticCall, get_insight
from src.db import MongoCollection, get_table
from src.helpers import get_today_date, ist_now
from src.notification import WhatsappNotification
from src.utils import LiveRateScrapper, logger, run_scrapper


def main():
    """
    Daily job to scrape metal rates, perform validation, generate insights and send whatsapp notification.
    """

    logger.info("✨ Daily execution started...")

    # Collection Initialization
    metal_rate_collection = get_table(name="metal_rate", collection_class=MongoCollection)
    insight_collection = get_table(name="insight", collection_class=MongoCollection)
    job_tracker_collection = get_table(name="job_tracker", collection_class=MongoCollection)

    scraped_data = None
    try:
        # Running scrapper
        scraped_data = run_scrapper(scrapper=LiveRateScrapper())

        #Data validation
        items = scraped_data.get("items", [])
        if not items:
            raise ValueError("No items found in scraped data.")

        rates = [rate for item in items for rate in item.get("rates", [])]
        if not rates:
            raise ValueError("No rates found in scraped data")


        # Loading rates in 'metal_rate' collection in DB based on data availability
        current_rate = items[0]["rates"]
        current_date = get_today_date()
        previous_rates_exist = metal_rate_collection.find_many(query={"date": {"$lt": current_date}}, ignore_defaults=True)

        if not previous_rates_exist:
            metal_rate_collection.insert_many(documents=rates)
        else:
            metal_rate_collection.insert_many(documents=current_rate)


        # Insight Generation & loading to 'insight' collection in DB
        daily_insight = get_insight(type="daily", agent=GeminiInsightAgenticCall(), data=scraped_data) or ""
        if not daily_insight:
            raise ValueError(f"No daily insight generated for {current_date}")

        insight_collection.insert_one({
            "status": "success",
            "message": daily_insight,
            "type": "daily",
            "sent_at": datetime.now(timezone.utc)
        })

        # sending daily insight Whatsapp Notifcation
        whatsapp = WhatsappNotification()
        whatsapp.send(data=daily_insight, type="daily")

        # capturing stats in 'Job Tracker' collection for scrapper job
        job_tracker_collection.insert_one({
            "scraped_at": scraped_data.get("scraped_at", ist_now()),
            "source": scraped_data.get("source", "N/A"),
            "status": "success"
        })
        logger.info("✅ Daily execution completed.")

    except Exception as e:
        logger.error(f"Daily execution failed: {type(e).__name__}: {str(e)}")

        # capturing failure in 'Job Tracker' collection for scrapper job
        job_tracker_collection.insert_one({
            "scraped_at": scraped_data.get("scraped_at", ist_now()),
            "source": scraped_data.get("source", "N/A"),
            "status": "failure",
            "reason": f"{type(e).__name__}: {str(e)}"
        })


if __name__ == "__main__":
    main()
