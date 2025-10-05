from datetime import date, datetime
from typing import List, Literal, Optional

from pydantic import BaseModel


class Metal(BaseModel):
    date: date
    type: Literal["gold", "silver"]
    purity: Optional[Literal["24k", "22k"]] = None
    price_per_g: float
    diff: float = 0
    percent: float = 0
    source: str


class Item(BaseModel):
    rates: List[Metal] = []


class MetalRate(BaseModel):
    scraped_at: datetime
    source: str
    items: List[Item] = []
    last_updated: Optional[dict] = {}


"""
Format:
{
  "scraped_at": "2025-09-16 12:08:30",
  "source": "live_rate",
  "last_updated": {
    "gold": "09:25:31 AM",
    "silver": "09:25:31 AM"
  }
  "items": [
    {
      "rates": [
          {
            "date": "2025-09-16",
            "type": "gold",
            "purity": "24k",
            "price_per_g": 144,
            "diff": 1,
            "percent": 0.7,
            "source": "live_rate",
          },
          {
            "date": "2025-09-16",
            "type": "gold",
            "purity": "22k",
            "price_per_g": 144,
            "diff": 1,
            "percent": 0.7,
            "source": "live_rate",
          },
          {
            "date": "2025-09-16",
            "type": "silver",
            "price_per_g": 144,
            "diff": 1,
            "percent": 0.7,
            "source": "live_rate",
          }
      ]
    },
    {
      "rates": [
          {
            "date": "2025-09-15",
            "type": "gold",
            "purity": "24k",
            "price_per_g": 144,
            "diff": 1,
            "percent": 0.7,
            "source": "live_rate",
          },
          {
            "date": "2025-09-15",
            "type": "gold",
            "purity": "22k",
            "price_per_g": 144,
            "diff": 1,
            "percent": 0.7,
            "source": "live_rate",
          },
          {
            "date": "2025-09-15",
            "type": "silver",
            "price_per_g": 144,
            "diff": 1,
            "percent": 0.7,
            "source": "live_rate",
          }
      ]
    }
  ]
}
"""
