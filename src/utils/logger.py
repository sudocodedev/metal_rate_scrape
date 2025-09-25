import logging
import logging.config

from src.settings import env

CONFIG = {
    "version": 1,
    "formatters": {
        "detailed": {"format": "%(asctime)s - %(module)s - %(levelname)s - L[%(lineno)d]: %(message)s"}
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
    if env == "prod":
        # integrate sentry
        pass
    return logging.getLogger("metal_rate")


logger = setup_logger()
