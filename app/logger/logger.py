import logging
import logging.config

from app.logger.config import LOGGER_CONFIG


def setup_logger():
  logging.config.dictConfig(LOGGER_CONFIG)
  return logging.getLogger("app")

logger = setup_logger()
