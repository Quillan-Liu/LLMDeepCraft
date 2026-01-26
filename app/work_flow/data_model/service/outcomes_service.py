from pathlib import Path

from app.logger.logger import logger
from app.utils.outcome_handler import outcome_querier, outcome_writer
from app.utils.schema_verifier import validate_json_str
from app.work_flow.data_model.chain.prompts.data_model_templates import \
  DATA_ENTITY_VALIDATION_SCHEMA
from app.work_flow.data_model.schemas.dto_schemas.data_model_requests import \
  DataModelGenerateRequest, DataModelSaveRequest, DataModelRequest
from app.work_flow.data_model.schemas.dto_schemas.data_model_response import \
  DataModelResponse

draft_path = Path("./work_flow/data_model/outcomes/draft")
draft_file_path = draft_path / "data_model_draft.json"
result_path = Path("./work_flow/data_model/outcomes/result")
result_file_path = result_path / "data_model_result.json"

def query_data_model_draft() -> DataModelResponse:
  logger.info("开始获取数据模型草稿")
  draft_content = outcome_querier(draft_file_path)
  draft = DataModelResponse.model_validate_json(draft_content)
  logger.info("成功获取数据模型草稿")
  return draft

def query_data_model_result() -> DataModelResponse:
  logger.info("开始获取数据模型成果")
  result_content = outcome_querier(result_file_path)
  result = DataModelResponse.model_validate_json(result_content)
  logger.info("成功获取用户故事成果")
  return result


async def update_data_model_draft(modified_draft: DataModelRequest) -> None:
  logger.info("开始上传被修改的数据模型草稿")
  content = modified_draft.model_dump(include={"entities", "relationships"}, mode="json")
  is_success, info_str = validate_json_str(content, DATA_ENTITY_VALIDATION_SCHEMA)
  if not is_success:
    logger.error(info_str)
  await outcome_writer(draft_file_path, content)
  logger.info("成功修改数据模型草稿")


async def save_data_model_draft(request: DataModelSaveRequest) -> None:
  if request.save_as_draft:
    logger.info("保存草稿")
    draft_path.mkdir(parents=True, exist_ok=True)
    await outcome_writer(draft_file_path,
                         request.model_dump(
                             include={"entities", "relationships"},
                             mode="json"
                         ))
  elif request.save_as_result:
    logger.info("将草稿储存为成果")
    result_path.mkdir(parents=True, exist_ok=True)
    await outcome_writer(result_file_path,
                         request.model_dump(
                             include={"entities", "relationships"},
                             mode="json"
                         ))
  else:
    logger.info("放弃储存草稿")