from typing import List

from pydantic import BaseModel, model_validator

from app.logger.logger import logger
from app.work_flow.data_model.schemas.domain_schemas.data_model_domains import \
  DataEntity, EntityRelationship
from app.work_flow.user_story.schemas.domain_schemas.user_story_domains import \
  UserStories


class DataModelGenerateRequest(BaseModel):
  user_story_result: UserStories
  human_requirements: str


class DataModelRequest(BaseModel):
  entities: List[DataEntity]
  relationships: List[EntityRelationship]


class DataModelSaveRequest(BaseModel):
  save_as_draft: bool
  save_as_result: bool
  not_save: bool
  entities: List[DataEntity]
  relationships: List[EntityRelationship]

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

