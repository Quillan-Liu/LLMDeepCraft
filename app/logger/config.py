

LOGGER_CONFIG = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "standard": {
      "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
      "datefmt": "%Y-%m-%d %H:%M:%S"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "formatter": "standard",
      "level": "INFO",
      "stream": "ext://sys.stdout"
    },
  },
  "root": {
    "level": "INFO",
    "handlers": ["console"]
  },
  "loggers": {
    "app": {
      "handlers": ["console"],
      "level": "INFO",
      "propagate": False,
    }
  }
}