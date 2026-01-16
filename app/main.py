from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import PlainTextResponse

from app.chains.converter_chains import query_md_result
from app.chains.design_chains import generate_project_design
from app.schemas.final_result_schemas import FullProjectDesign
import os
from dotenv import load_dotenv
from app.history_manager import history_manager

# Load environment variables
load_dotenv()
app = FastAPI(
    title="LLM Requirement Processing API",
    description="Converts natural language requirements into structured software design documents.",
    version="0.1.0"
)


class DesignRequest(BaseModel):
  requirements: str

@app.get("/")
async def root():
  return {
    "message": "Welcome to LLM Architect. Use /design to generate project designs."
  }


@app.post("/design", response_model=FullProjectDesign)
async def design_project(request: DesignRequest) -> FullProjectDesign:
  """
  Takes natural language requirements and returns a full project design
  (User Stories, Data Model, System Modules).
  """
  if not os.getenv("OPENAI_API_KEY"):
    raise HTTPException(status_code=500,
                        detail="环境变量中未设置 OPENAI_API_KEY")

  try:
    result = await generate_project_design(request.requirements)
    history_manager.save_history_record(result)
    return result
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@app.post("/convert/json_to_md", response_model=str)
async def convert_json_to_md(request: FullProjectDesign) -> PlainTextResponse:
  result = await query_md_result(request)
  return PlainTextResponse(result)


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="127.0.0.1", port=8000)