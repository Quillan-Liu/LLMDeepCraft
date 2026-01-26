from fastapi import FastAPI, HTTPException
from starlette.responses import PlainTextResponse

from app.logger.logger import logger
from dotenv import load_dotenv

from app.work_flow.data_model.chain.data_model_chain import \
  generate_data_model_draft, modify_data_model_draft, data_model_json_to_md
from app.work_flow.data_model.schemas.dto_schemas.data_model_requests import \
  DataModelGenerateRequest, DataModelSaveRequest, DataModelRequest
from app.work_flow.data_model.schemas.dto_schemas.data_model_response import \
  DataModelResponse
from app.work_flow.data_model.service.outcomes_service import \
  query_data_model_draft, query_data_model_result, update_data_model_draft, \
  save_data_model_draft
from app.work_flow.user_story.chain.user_story_chain import \
  generate_user_stories, modify_user_stories_draft, user_stories_json_to_md
from app.work_flow.user_story.schemas.dto_schemas.user_story_requests import \
  UserStoryUpdateRequest, UserStoryRequest, UserStoryGenerateRequest, \
  UserStorySaveRequest
from app.work_flow.user_story.schemas.dto_schemas.user_story_response import \
  UserStoriesResponse
from app.work_flow.user_story.service.outcomes_service import (
  update_user_stories_draft, save_user_stories_draft, query_user_stories_draft,
  query_user_stories_result)

# Load environment variables
load_dotenv()
app = FastAPI(
    title="LLM Requirement Processing API",
    description="Converts natural language requirements into structured software design documents.",
    version="0.1.0"
)


@app.get("/")
async def root():
  return {
    "message": "Welcome to LLM Architect. Use /design to generate project designs."
  }


@app.post("/user_stories/json_to_md", response_class=PlainTextResponse)
async def convert_json_to_md(request: UserStoryRequest) -> PlainTextResponse:
  result = await user_stories_json_to_md(request)
  return PlainTextResponse(result)


@app.post("/user_stories/generate", response_model=UserStoriesResponse)
async def user_stories_generation(request: UserStoryGenerateRequest) -> UserStoriesResponse:
  try:
    user_stories = await generate_user_stories(request)
    return user_stories
  except Exception as e:
    logger.error(str(e))
    raise HTTPException(status_code=500, detail=str(e))


@app.get("/user_stories/query/draft", response_model=UserStoriesResponse)
async def user_stories_draft_querier() -> UserStoriesResponse:
  try:
    draft = query_user_stories_draft()
    return draft
  except Exception as e:
    logger.error(str(e))
    raise HTTPException(status_code=500, detail=str(e))


@app.get("/user_stories/query/result", response_model=UserStoriesResponse)
async def user_stories_result_querier() -> UserStoriesResponse:
  try:
    result = query_user_stories_result()
    return result
  except Exception as e:
    logger.error(str(e))
    raise HTTPException(status_code=500, detail=str(e))


@app.post("/user_stories/modify", response_model=UserStoriesResponse)
async def user_stories_modification(request: UserStoryUpdateRequest) -> UserStoriesResponse:
  try:
    updated_user_stories = await modify_user_stories_draft(request)
    return updated_user_stories
  except Exception as e:
    logger.error(str(e))
    raise HTTPException(status_code=500, detail=str(e))


@app.post("/user_stories/update/draft", response_model=None)
async def user_stories_draft_update(request: UserStoryRequest) -> None:
  try:
    await update_user_stories_draft(request)
  except Exception as e:
    logger.error(str(e))
    raise HTTPException(status_code=500, detail=str(e))


@app.post("/user_stories/save/draft", response_model=None)
async def user_stories_save_draft(request: UserStorySaveRequest) -> None:
  try:
    await save_user_stories_draft(request)
  except Exception as e:
    logger.error(str(e))
    raise HTTPException(status_code=500, detail=str(e))


@app.post("/data_model/json_to_md", response_class=PlainTextResponse)
async def convert_json_to_md(request: DataModelRequest) -> PlainTextResponse:
  result = await data_model_json_to_md(request)
  return PlainTextResponse(result)


@app.post("/data_model/generate", response_model= DataModelResponse)
async def data_model_generation(data_model_requirement: DataModelGenerateRequest) -> DataModelResponse:
  try:
    data_model = await generate_data_model_draft(data_model_requirement)
    return data_model
  except Exception as e:
    logger.error(str(e))
    raise HTTPException(status_code=500, detail=str(e))


@app.post("/data_model/modify", response_model= DataModelResponse)
async def data_model_modification(data_model_requirement: DataModelGenerateRequest) -> DataModelResponse:
  try:
    data_model = await modify_data_model_draft(data_model_requirement)
    return data_model
  except Exception as e:
    logger.error(str(e))
    raise HTTPException(status_code=500, detail=str(e))


@app.get("/data_model/query/draft", response_model=DataModelResponse)
async def data_model_draft_querier() -> DataModelResponse:
  try:
    draft = query_data_model_draft()
    return draft
  except Exception as e:
    logger.error(str(e))
    raise HTTPException(status_code=500, detail=str(e))


@app.get("/data_model/query/result", response_model=DataModelResponse)
async def user_stories_result_querier() -> DataModelResponse:
  try:
    result = query_data_model_result()
    return result
  except Exception as e:
    logger.error(str(e))
    raise HTTPException(status_code=500, detail=str(e))


@app.post("/data_model/update/draft", response_model=None)
async def data_model_draft_update(request: DataModelRequest) -> None:
  try:
    await update_data_model_draft(request)
  except Exception as e:
    logger.error(str(e))
    raise HTTPException(status_code=500, detail=str(e))


@app.post("/data_model/save/draft", response_model=None)
async def data_model_save_draft(request: DataModelSaveRequest) -> None:
  try:
    await save_data_model_draft(request)
  except Exception as e:
    logger.error(str(e))
    raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="127.0.0.1", port=8000)