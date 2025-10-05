import random
from datetime import date, datetime, timedelta, timezone
from typing import Optional, Tuple

from src.settings import USER_AGENTS


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


def ist_now():
    IST = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(IST).isoformat()

def get_today_date():
    return datetime.now().date().isoformat()

def get_start_end_week_dates() -> Tuple[str, str]:
    today = datetime.now(timezone.utc).date()
    start_date = today - timedelta(days=today.weekday()) # mon
    end_date = start_date + timedelta(days=6) # sun
    return start_date.isoformat(), end_date.isoformat()

def utc_now():
    return datetime.now(timezone.utc)


def start_end_of_today():
    st_dt = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    end_dt = st_dt + timedelta(days=1)
    return st_dt, end_dt
