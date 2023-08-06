import logging  # noqa
import os


def default_logging_configuration(logging_dir, logging_level="INFO"):
    return {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(name)s:%(lineno)d %(levelname)s - %(message)s",
            },
            "collector": {
                "format": "%(asctime)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "formatter": "simple",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "graphite_feeder": {
                "formatter": "simple",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(logging_dir, "graphite-feeder.log"),
                "when": "midnight",
                "interval": 1,
            },
            "home": {
                "formatter": "simple",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(logging_dir, "graphite-home.log"),
                "when": "midnight",
                "interval": 1,
            },
        },
        "loggers": {
            "": {
                "level": "WARNING",
                "handlers": ["console", "graphite_feeder"],
                "propagate": True,
            },
            "asyncio": {
                "level": "WARNING",
                "handlers": ["console", "graphite_feeder"],
                "propagate": False,
            },
            "apscheduler": {
                "level": "WARNING",
                "handlers": ["console", "graphite_feeder"],
                "propagate": False,
            },
            "__main__": {
                "level": logging_level,
                "handlers": ["console", "graphite_feeder"],
                "propagate": False,
            },
            "graphite_feeder": {
                "level": logging_level,
                "handlers": ["console", "graphite_feeder"],
                "propagate": False,
            },
            "home": {
                "level": logging_level,
                "handlers": ["console", "home"],
                "propagate": False,
            },
        },
    }
