import json
from pathlib import Path

import aiofiles

from app.logger.logger import logger


def outcome_querier(outcome_path: Path) -> str:
  try:
    with open(outcome_path, "r", encoding='utf-8') as f:
      logger.info(f"开始获取路径为 {outcome_path} 的草稿")
      content = f.read()
      outcome = json.loads(content)
      formatted_outcome = json.dumps(outcome, indent=2, ensure_ascii=False)
      logger.info(f"成功获取路径为 {outcome_path} 的草稿")
      return formatted_outcome
  except FileNotFoundError as e:
    logger.error(f"{e}")
    raise e
  except json.decoder.JSONDecodeError as e:
    logger.error(f"{e}")
    raise e
  except Exception as e:
    logger.error(f"{e}")
    raise e


async def outcome_writer(outcome_path: Path, content: dict) -> None:
  try:
    async with aiofiles.open(outcome_path, "w", encoding='utf-8') as f:
      logger.info(f"开始向路径为 {outcome_path} 的文件写入内容")
      await f.write(json.dumps(content, indent=2, ensure_ascii=False))
      logger.info(f"成功向路径为 {outcome_path} 的文件写入内容")
  except FileNotFoundError as e:
    logger.error(f"{e}")
    raise e
  except json.decoder.JSONDecodeError as e:
    logger.error(f"{e}")
    raise e
  except Exception as e:
    logger.error(f"{e}")
    raise e