import os

from dotenv import load_dotenv

load_dotenv()

# Random User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
]

# Scrapping config
LIVE_RATE_URL = os.getenv("LIVE_RATE_URL")
SCRAPER = "live_rate"

# Agentic AI config
ALLOW_AGENT_CALL = os.getenv("MAKE_AGENT_CALL", "False") == "True"
AI_AGENT_API_KEY = os.getenv("AI_AGENT_API_KEY")
AI_AGENT_MODEL = os.getenv("AI_AGENT_MODEL")

# MongoDB config
URI = os.getenv("URI")
DB = os.getenv("DB")

# Environment
env = os.getenv("ENV", "dev")

# Whatsapp config
WHAPI_URL = os.getenv("WHAPI_URL", "")
WHAPI_TOKEN = os.getenv("WHAPI_TOKEN", "")
WHAPI_GROUP_ID = os.getenv("WHAPI_GROUP_ID", "")
SEND_WHATSAPP_NOTIFICATION = os.getenv("SEND_WHATSAPP_NOTIFICATION", "False") == "True"

# Sentry Config
SENTRY_DSN = os.getenv("SENTRY_DSN", '')
