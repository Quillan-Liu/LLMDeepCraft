from typing import List

from pydantic import BaseModel, Field

class UserStory(BaseModel):
  function_name: str = Field(description="The name of the function")
  role: str = Field(description="The actor in the story (e.g., User, Admin)")
  action: str = Field(description="What the actor wants to do")
  value: str = Field(description="The benefit or value of the action")
  acceptance_criteria: List[str] = Field(
    description="List of criteria to verify the story is done")

class UserStories(BaseModel):
  stories: List[UserStory]


