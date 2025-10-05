from datetime import datetime, timezone

from src.agent import GeminiInsightAgenticCall, get_insight
from src.db import MongoCollection, get_table
from src.helpers import get_today_date, ist_now, start_end_of_today
from src.notification import WhatsappNotification
from src.utils import LiveRateScrapper, logger, run_scrapper


def main():
    """
    Evening rate update job to check if there are any changes in the metal rates, generating insight
    and sent whatsapp notification.
    """

    logger.info("✨ Daily Evening rate update check execution started...")

    # Collection Initialization
    metal_rate_collection = get_table(name="metal_rate", collection_class=MongoCollection)
    insight_collection = get_table(name="insight", collection_class=MongoCollection)
    job_tracker_collection = get_table(name="job_tracker", collection_class=MongoCollection)

    scraped_data = None
    try:
        current_date = get_today_date()
        last_run = job_tracker_collection.find_one(
            query={
                "source": "live_rate",
                "status": "success",
                "is_active": True,
                "scraped_at": {"$regex": f"^{current_date}"}
            }
        )
        if not last_run:
            logger.info("No successful job found for today, skipping evening update.")
            return None

        # scrape current data
        scraped_data = run_scrapper(scrapper=LiveRateScrapper())
        last_updated = scraped_data.get("last_updated", {})

        # Getting last update time from DB and site
        gold_site_upd_tm, silver_site_upd_tm = last_updated.get("gold"), last_updated.get("silver")
        gold_db_upd_tm, silver_db_upd_tm = last_run.get("gold_last_upd_tm"), last_run.get("silver_last_upd_tm")

        # Checking the exit flow
        if not all([gold_db_upd_tm, silver_db_upd_tm, gold_site_upd_tm, silver_site_upd_tm]):
            logger.error(
                f"Missing timings - DB: gold={gold_db_upd_tm}, silver={silver_db_upd_tm} | Site: gold={gold_site_upd_tm}, silver={silver_site_upd_tm}"
            )
            logger.error("❌ Execution stopped...")
            return None

        if (gold_site_upd_tm == gold_db_upd_tm) and (silver_site_upd_tm == silver_db_upd_tm):
            logger.error("No newer updates found in the site.")
            logger.error("✅ Exiting the execution...")
            return None

        #Data validation
        items = scraped_data.get("items", [])
        if not items:
            raise ValueError("No items found in scraped data.")

        # Updating the rates if diff found.
        current_rate = items[0]["rates"]
        for rate in current_rate:
            metal_rate_collection.update_one(
                query={
                    "date": rate.get("date"),
                    "type": rate.get("type"),
                    "source": rate.get("source"),
                    "is_active": True,
                    "purity": rate.get("purity")
                },
                update={
                    "$set": {"price_per_g": rate.get("price_per_g", 0.0)}
                }
            )

        # Querying the mrng generated insight from DB
        start_dt, end_dt = start_end_of_today()
        mrng_insight = insight_collection.find_one(
            query={
                "status": "success",
                "is_active": True,
                "type": "daily",
                "sent_at": {"$gte": start_dt, "$lt": end_dt}
            }
        )

        # Insight Generation & loading to 'insight' collection in DB
        data = {"rates": current_rate, "mrng_insight": mrng_insight.get("message", "")}
        evening_insight = get_insight(type="evening", agent=GeminiInsightAgenticCall(), data=data) or ""
        if not evening_insight:
            raise ValueError(f"No daily insight generated for {current_date}")

        insight_id = insight_collection.insert_one({
            "status": "success",
            "message": evening_insight,
            "type": "evening",
            "sent_at": datetime.now(timezone.utc)
        })

        # sending daily insight Whatsapp Notifcation
        whatsapp = WhatsappNotification()
        whatsapp.send(data=evening_insight, type="evening")

        # capturing stats in 'Job Tracker' collection for scrapper job
        job_tracker_collection.insert_one({
            "scraped_at": scraped_data.get("scraped_at", ist_now()),
            "source": scraped_data.get("source", "N/A"),
            "status": "success",
            "gold_last_upd_tm": gold_site_upd_tm,
            "silver_last_upd_tm": silver_site_upd_tm,
            "insight": insight_id
        })
        logger.info("✅ Daily Evening rate update check execution completed...")


    except Exception as e:
        logger.error(f"Daily execution failed: {type(e).__name__}: {str(e)}")

        # capturing failure in 'Job Tracker' collection for scrapper job
        job_tracker_collection.insert_one({
            "scraped_at": scraped_data.get("scraped_at", ist_now()),
            "source": scraped_data.get("source", "N/A"),
            "status": "failure",
            "reason": f"{type(e).__name__}: {str(e)}",
            "gold_last_upd_tm": scraped_data.get("last_updated", {}).get("gold"),
            "silver_last_upd_tm": scraped_data.get("last_updated", {}).get("silver"),
        })


if __name__ == "__main__":
    main()
