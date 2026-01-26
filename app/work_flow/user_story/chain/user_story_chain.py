from pathlib import Path

import aiofiles
import json

from langchain_core.output_parsers import StrOutputParser

from app.logger.logger import logger
from app.work_flow.user_story.chain.prompts.user_stories_templates import \
  USER_STORY_VALIDATION_SCHEMA
from app.work_flow.user_story.chain.prompts.user_story_prompts import \
  STORY_GENERATION_PROMPT, STORY_UPDATE_PROMPT, JSON_TO_MD_PROMPT
from app.LLMs.LLM import llm
from app.work_flow.user_story.schemas.dto_schemas.user_story_requests import \
  UserStoryGenerateRequest, UserStoryUpdateRequest, UserStoryRequest
from app.work_flow.user_story.schemas.dto_schemas.user_story_response import \
  UserStoriesResponse
from app.utils.base_model_converter import base_model_to_dict
from app.utils.env_validator import env_varies_validator
from app.utils.outcome_handler import outcome_querier
from app.utils.schema_verifier import validate_json_str


draft_path = Path("./work_flow/user_story/outcomes/draft")
draft_file_path = draft_path / "user_stories_draft.json"


generate_story_chain = (
    STORY_GENERATION_PROMPT
    | llm.with_structured_output(UserStoriesResponse)
)

update_user_story_chain = (
  STORY_UPDATE_PROMPT
  | llm.with_structured_output(UserStoriesResponse)
)

json_to_md_chain = (
  JSON_TO_MD_PROMPT
  | llm
  | StrOutputParser()
)


async def generate_user_stories(
    user_stories_requirements: UserStoryGenerateRequest
) -> UserStoriesResponse:
  env_varies_validator()
  logger.info("开始生成用户故事")
  stories_result = await (generate_story_chain
                          .ainvoke({"user_stories_requirements": user_stories_requirements}))
  stories_result_dict = user_story_format_verifier(stories_result)
  await write_user_stories_draft(stories_result_dict)
  logger.info("用户故事生成完成")
  return stories_result


async def modify_user_stories_draft(
    user_stories_requirements: UserStoryUpdateRequest
) -> UserStoriesResponse:
  env_varies_validator()
  draft = outcome_querier(draft_file_path)
  logger.info("开始根据草稿修改用户故事")
  updated_user_stories_result = await (update_user_story_chain
                                       .ainvoke({
    "user_stories_draft": draft,
    "user_stories_modification_suggestions": user_stories_requirements
  }))
  user_story_format_verifier(updated_user_stories_result)
  logger.info("成功根据草稿修改用户故事")
  return updated_user_stories_result


async def write_user_stories_draft(stories_result_dict: dict) -> None:
  logger.info("开始记录用户故事的草稿")

  draft_path.mkdir(parents=True, exist_ok=True)

  try:
    async with aiofiles.open(draft_file_path, "w", encoding="utf-8") as f:
      content = json.dumps(stories_result_dict, indent=2, ensure_ascii=False)
      await f.write(content)
  except OSError as e:
    logger.error(f"写入用户故事草稿文件失败：{e}")


async def user_stories_json_to_md(user_stories: UserStoryRequest) -> str:
  logger.info("开始将用户故事的 json 转为 md 格式")
  user_stories_json = base_model_to_dict(user_stories)
  md_result = await json_to_md_chain.ainvoke({"result_json": user_stories_json})
  logger.info("成功将用户故事的 json 转为 md 格式")
  return md_result

def user_story_format_verifier(llm_result: UserStoriesResponse) -> dict:
  result_dict = base_model_to_dict(llm_result)
  if not validate_json_str(result_dict, USER_STORY_VALIDATION_SCHEMA):
    logger.error("生成的用户故事格式错误")
    raise ValueError("生成的用户故事格式错误")
  return result_dict


if __name__ == "__main__":
  import asyncio

  # 示例原始需求
  sample_requirements = """
        We need a task management application for small teams.
        Users should be able to create projects, add tasks to projects,
        assign tasks to team members, set due dates, and mark tasks as complete.
        The app should support real-time updates and user authentication.
        """


  async def main():
    try:
      result = await generate_user_stories(sample_requirements)

    except Exception as e:
      print(f"❌ Error during generation: {e}")
      raise

    formatted_json = json.dumps(result.model_dump(), indent=2, ensure_ascii=False)
    print(formatted_json)


  # Run the async function
  asyncio.run(main())