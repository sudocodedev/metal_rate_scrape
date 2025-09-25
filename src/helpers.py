import locale
import random
from datetime import date, datetime, timedelta, timezone
from typing import Optional

from src.settings import USER_AGENTS

locale.setlocale(locale.LC_MONETARY, "en_IN")


def user_agent() -> str:
    return random.choice(USER_AGENTS)


def parse_float(data: str) -> float:
    try:
        return float(data.replace(",", "").strip())
    except (ValueError, TypeError):
        return 0.0


def parse_date(data: str, format: str = "%d/%b/%Y") -> Optional[date]:
    try:
        dt = datetime.strptime(str(data).strip(), format)
        return dt.date().isoformat()
    except (ValueError, TypeError):
        return None


def compute_percent(data1: float, data2: float) -> float:
    return round(((data1 - data2) / data2) * 100, 2)


def format_currentcy(amount: float) -> str:
    return locale.currency(amount, grouping=True)


def ist_now():
    IST = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(IST).isoformat()
