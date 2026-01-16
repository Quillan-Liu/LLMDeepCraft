from langchain_core.output_parsers import StrOutputParser

from app.chains.LLM import llm
from app.prompts.json_to_md_prompts import JSON_TO_MD_PROMPT
from app.schemas.final_result_schemas import FullProjectDesign
from app.schemas.utils import base_model_converter

json_to_md_chain = (
  JSON_TO_MD_PROMPT
  | llm
  | StrOutputParser()
)


async def query_md_result(result_json: FullProjectDesign) -> str:
  full_project_design = base_model_converter.base_model_to_json(result_json)
  md_result = await json_to_md_chain.ainvoke(
      {"result_json": full_project_design})

  return md_result

