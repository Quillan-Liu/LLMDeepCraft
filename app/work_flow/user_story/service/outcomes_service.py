from pathlib import Path

from app.logger.logger import logger
from app.utils.base_model_converter import base_model_to_dict
from app.work_flow.user_story.chain.prompts.user_stories_templates import \
  USER_STORY_VALIDATION_SCHEMA
from app.work_flow.user_story.schemas.dto_schemas.user_story_requests import \
  UserStoryRequest, UserStorySaveRequest
from app.work_flow.user_story.schemas.dto_schemas.user_story_response import \
  UserStoriesResponse
from app.utils.outcome_handler import outcome_querier, outcome_writer
from app.utils.schema_verifier import validate_json_str

draft_path = Path("./work_flow/user_story/outcomes/draft")
draft_file_path = draft_path / "user_stories_draft.json"
result_path = Path("./work_flow/user_story/outcomes/result")
result_file_path = result_path / "user_stories_result.json"

def query_user_stories_draft() -> UserStoriesResponse:
  logger.info("开始获取用户故事草稿")
  draft_content = outcome_querier(draft_file_path)
  draft = UserStoriesResponse.model_validate_json(draft_content)
  logger.info("成功获取用户故事草稿")
  return draft

def query_user_stories_result() -> UserStoriesResponse:
  logger.info("开始获取用户故事成果")
  result_content = outcome_querier(result_file_path)
  result = UserStoriesResponse.model_validate_json(result_content)
  logger.info("成功获取用户故事成果")
  return result


async def update_user_stories_draft(modified_draft: UserStoryRequest) -> None:
  logger.info("开始上传被修改的用户故事草稿")
  modified_draft_dict = base_model_to_dict(modified_draft)
  is_success, info_str = validate_json_str(modified_draft_dict, USER_STORY_VALIDATION_SCHEMA)
  if not is_success:
    logger.error(info_str)
  await outcome_writer(draft_file_path, modified_draft_dict)
  logger.info("成功修改故事草稿")


async def save_user_stories_draft(request: UserStorySaveRequest) -> None:
  if request.save_as_draft:
    logger.info("保存草稿")
    draft_path.mkdir(parents=True, exist_ok=True)
    await outcome_writer(draft_file_path,
                         request.user_stories_draft.model_dump())
  elif request.save_as_result:
    logger.info("将草稿储存为成果")
    result_path.mkdir(parents=True, exist_ok=True)
    await outcome_writer(result_file_path,
                         request.user_stories_draft.model_dump())
  else:
    logger.info("放弃储存草稿")