from typing import List
from pydantic import BaseModel

from app.schemas.data_entity_schemas import DataModelResponse
from app.schemas.system_design_schemas import SystemDesignResponse
from app.schemas.user_story_shemas import UserStory


class FullProjectDesign(BaseModel):
    user_stories: List[UserStory]
    data_model: DataModelResponse
    system_design: SystemDesignResponse
