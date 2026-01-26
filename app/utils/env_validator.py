import os

from fastapi import HTTPException

from app.logger.logger import logger


def env_varies_validator():
  if not os.getenv("OPENAI_API_KEY"):
    logger.error("环境变量中未设置 OPENAI_API_KEY")
    raise HTTPException(status_code=500,
                        detail="环境变量中未设置 OPENAI_API_KEY")