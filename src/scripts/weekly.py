from datetime import datetime, timezone

from src.agent import GeminiInsightAgenticCall, get_insight
from src.db import MongoCollection, SortOrder, get_table
from src.helpers import get_start_end_week_dates
from src.notification import WhatsappNotification
from src.settings import SCRAPER
from src.utils import logger


def get_weekly_rates(rate, insight) -> dict:
    """
    Creates a dict with current week's metal rates along with last week's insight if available
    """
    start_dt, end_dt = get_start_end_week_dates()

    # fetching gold rates for entire week
    gold_rates = rate.find_many(
        query={
            "date": {"$gte": start_dt, "$lte": end_dt},
            "type": "gold",
            "source": SCRAPER
        },
        ignore_defaults=True
    )

    # fetching silver rates for entire week
    silver_rates = rate.find_many(
        query={
            "date": {"$gte": start_dt, "$lte": end_dt},
            "type": "silver",
            "source": SCRAPER
        },
        ignore_defaults=True
    )

    # fetching last week's insight if available
    last_week_insight = insight.find_one(query={"type": "weekly", "is_active": True},  sort=[("created_at", SortOrder.DESC)])

    return {
        "gold": gold_rates,
        "silver": silver_rates,
        "insight": last_week_insight.get("message", "") if isinstance(last_week_insight, dict) else ""
    }

def main():
    """
    Weekly job to fetch current week's rates from DB, generate insights and send whatsapp notification.
    """

    logger.info("✨ Weekly execution started...")

    try:
        # collection Initialization
        metal_rate_collection = get_table(name="metal_rate", collection_class=MongoCollection)
        insight_collection = get_table(name="insight", collection_class=MongoCollection)

        # Rates query
        data = get_weekly_rates(rate=metal_rate_collection, insight=insight_collection)

        # Insight Generation & loading to 'insight' collection in DB
        weekly_insight = get_insight(type="weekly", agent=GeminiInsightAgenticCall(), data=data) or ""
        insight_collection.insert_one({
            "status": "success",
            "message": weekly_insight,
            "type": "weekly",
            "sent_at": datetime.now(timezone.utc)
        })

        # sending daily insight Whatsapp Notifcation
        whatsapp = WhatsappNotification()
        whatsapp.send(data=weekly_insight, type="weekly")
        logger.info("✅ Weekly execution completed.")

    except Exception as e:
        logger.error(f"{type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    main()
