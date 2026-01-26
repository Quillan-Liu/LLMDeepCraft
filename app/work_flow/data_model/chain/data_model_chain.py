import json
from pathlib import Path

import aiofiles
from langchain_core.output_parsers import StrOutputParser

from app.LLMs.LLM import llm
from app.logger.logger import logger
from app.utils.base_model_converter import base_model_to_dict
from app.utils.outcome_handler import outcome_querier
from app.utils.schema_verifier import validate_json_str
from app.work_flow.data_model.chain.prompts.data_model_prompts import \
  DATA_MODEL_GENERATION_PROMPT, DATA_MODEL_MODIFICATION_PROMPT, \
  JSON_TO_MD_PROMPT
from app.work_flow.data_model.chain.prompts.data_model_templates import \
  DATA_ENTITY_VALIDATION_SCHEMA
from app.work_flow.data_model.schemas.dto_schemas.data_model_requests import \
  DataModelGenerateRequest, DataModelRequest
from app.work_flow.data_model.schemas.dto_schemas.data_model_response import \
  DataModelResponse


draft_path = Path("./work_flow/data_model/outcomes/draft")
draft_file_path = draft_path / "data_model_draft.json"


data_model_generation_chain = (
    DATA_MODEL_GENERATION_PROMPT
    | llm.with_structured_output(DataModelResponse)
)


data_model_modification_chain = (
  DATA_MODEL_MODIFICATION_PROMPT
  | llm.with_structured_output(DataModelResponse)
)

json_to_md_chain = (
  JSON_TO_MD_PROMPT
  | llm
  | StrOutputParser()
)


async def generate_data_model_draft(
    data_model_requirement: DataModelGenerateRequest
) -> DataModelResponse:
  logger.info("开始根据用户故事生成数据模型")
  human_requirements = data_model_requirement.human_requirements
  if human_requirements == "":
    human_requirements = "用户无额外要求，直接生成数据模型即可。"
  user_story_result = data_model_requirement.user_story_result
  data_model_result = await data_model_generation_chain.ainvoke(
      {
        "user_story_result": user_story_result,
        "user_requirements": human_requirements,
      }
  )

  data_model_dict = data_model_format_verifier(data_model_result)
  await write_data_model_draft(data_model_dict)
  logger.info("数据模型生成完成")

  return data_model_result


async def modify_data_model_draft(
    data_model_requirement: DataModelGenerateRequest
) -> DataModelResponse:
  human_requirements = data_model_requirement.human_requirements
  user_story_result = data_model_requirement.user_story_result
  data_model_draft = outcome_querier(draft_file_path)
  logger.info("开始根据用户自然语言的需求修改数据模型草稿")
  modified_data_model_result = await (data_model_modification_chain
                                      .ainvoke({
    "user_story_result": user_story_result,
    "data_model_draft": data_model_draft,
    "user_requirements": human_requirements,
  }))
  data_model_format_verifier(modified_data_model_result)
  logger.info("成功根据用户自然语言的需求修改数据模型草稿")
  return modified_data_model_result


async def write_data_model_draft(data_model_dict: dict) -> None:
  logger.info("开始记录数据模型的草稿")

  draft_path.mkdir(parents=True, exist_ok=True)

  try:
    async with aiofiles.open(draft_file_path, "w", encoding="utf-8") as f:
      content = json.dumps(data_model_dict, indent=2, ensure_ascii=False)
      await f.write(content)
  except OSError as e:
    logger.error(f"写入用户故事草稿文件失败：{e}")


async def data_model_json_to_md(data_models: DataModelRequest) -> str:
  logger.info("开始将数据模型的 json 转为 md 格式")
  data_models_json = base_model_to_dict(data_models)
  md_result = await json_to_md_chain.ainvoke({"result_json": data_models_json})
  logger.info("成功将数据模型的 json 转为 md 格式")
  return md_result


def data_model_format_verifier(llm_result: DataModelResponse) -> dict:
  result_dict = base_model_to_dict(llm_result)
  if not validate_json_str(result_dict, DATA_ENTITY_VALIDATION_SCHEMA):
    logger.error("生成的数据模型格式错误")
    raise ValueError("生成的实体格式错误")
  return result_dict