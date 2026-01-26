from typing import List

from pydantic import BaseModel, model_validator

from app.logger.logger import logger
from app.work_flow.user_story.schemas.domain_schemas.user_story_domains import UserStory, \
  UserStories


class UserStoryGenerateRequest(BaseModel):
  requirements: str


class UserStoryUpdateRequest(BaseModel):
  requirements: str


class UserStoryRequest(BaseModel):
  stories: List[UserStory]


class UserStorySaveRequest(BaseModel):
  save_as_draft: bool
  save_as_result: bool
  not_save: bool
  user_stories_draft: UserStories

  @model_validator(mode="after")
  def validate_exclusive_options(self) -> "UserStorySaveRequest":
    true_count = sum([
      self.save_as_draft,
      self.save_as_result,
      self.not_save
    ])

    if true_count != 1:
      logger.error(
          "save_as_draft, save_as_result, not_save 中有且只有一个必须为 True"
      )
      raise ValueError(
          "save_as_draft, save_as_result, not_save 中有且只有一个必须为 True"
      )

    return self
