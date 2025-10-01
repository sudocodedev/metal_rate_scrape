import logging
import logging.config

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from src import settings

CONFIG = {
    "version": 1,
    "formatters": {
        "detailed": {"format": "%(asctime)s - %(module)s - %(levelname)s - %(message)s"}
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "level": "INFO", "formatter": "detailed"},
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "app.log",
        },
    },
    "loggers": {"metal_rate": {"handlers": ["console", "file"], "level": "DEBUG", "propagate": True}},
}


def setup_logger():
    logging.config.dictConfig(CONFIG)
    if settings.env == "prod":
        logging_integration = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            send_default_pii=False,
            enable_logs=True,
            environment=settings.env,
            integrations=[logging_integration]
        )
    return logging.getLogger("metal_rate")


logger = setup_logger()
