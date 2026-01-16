from app.chains.converter_chains import llm
from app.prompts.utils.prompts_vari_generator import generate_data_model_data
from app.schemas.data_entity_schemas import DATA_ENTITY_VALIDATION_SCHEMA, \
  DataModelResponse
from app.prompts.design_prompts import STORY_GENERATION_PROMPT, DATA_MODELING_PROMPT, \
  SYSTEM_DESIGN_PROMPT
from app.schemas.final_result_schemas import SystemDesignResponse, \
  FullProjectDesign
from app.schemas.utils.base_model_converter import base_model_to_dict, \
  dict_to_full_project_design
from app.schemas.utils.schema_verifier import validate_json_str
from app.schemas.user_story_shemas import USER_STORY_VALIDATION_SCHEMA, \
  UserStoriesResponse
from app.history_manager import history_manager

# Initialize the model (Assumes OPENAI_API_KEY is set in environment)
# using a lower temperature for more deterministic structural output

# --- Chain 1: User Stories ---
story_chain = (
    STORY_GENERATION_PROMPT
    | llm.with_structured_output(UserStoriesResponse)
)


# --- Chain 2: Data Modeling ---
data_model_chain = (
    DATA_MODELING_PROMPT
    | llm.with_structured_output(DataModelResponse)
)

# --- Chain 3: System Design ---
system_design_chain = (
    SYSTEM_DESIGN_PROMPT
    | llm.with_structured_output(SystemDesignResponse)
)


async def update_project_design(raw_requirements: str) -> FullProjectDesign:
  pass

# --- Main Orchestrator Function ---
async def generate_project_design(raw_requirements: str) -> FullProjectDesign:
  """
  Orchestrates the 3-step generation process.
  """

  # Step 1: Generate User Stories
  print("--- Generating User Stories ---")
  stories_result = await story_chain.ainvoke(
      {"raw_requirements": raw_requirements})

  stories_result_dict = base_model_to_dict(stories_result)
  if not validate_json_str(stories_result_dict, USER_STORY_VALIDATION_SCHEMA):
    raise ValueError("生成的用户故事格式错误")

  stories_text = "\n".join(
      [f"- {s["role"]} {s["action"]}, {s["value"]}"
       for s in stories_result_dict["stories"]])

  # # Step 2: Generate Data Model (using stories as context)
  print("--- Generating Data Model ---")
  data_model_result = await data_model_chain.ainvoke(
      {"user_stories": stories_text})

  data_model_dict = base_model_to_dict(data_model_result)
  if not validate_json_str(data_model_dict, DATA_ENTITY_VALIDATION_SCHEMA):
    raise ValueError("生成的实体格式错误")

  entities_text = generate_data_model_data(data_model_dict)

  # Step 3: Generate System Design (using stories + data model as context)
  print("--- Generating System Design ---")
  system_design_result = await system_design_chain.ainvoke({
    "user_stories": stories_text,
    "data_model": entities_text
  })
  system_design_dict = base_model_to_dict(system_design_result)

  result = dict_to_full_project_design(
      stories_result_dict,
      data_model_dict,
      system_design_dict)

  return result


if __name__ == "__main__":
  import json
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
      result = await generate_project_design(sample_requirements)

    except Exception as e:
      print(f"❌ Error during generation: {e}")
      raise

    formatted_json = json.dumps(result, indent=4, ensure_ascii=False)
    print(formatted_json)


  # Run the async function
  asyncio.run(main())
