from typing import List

from pydantic import BaseModel

from app.work_flow.user_story.schemas.domain_schemas.user_story_domains import UserStory


class UserStoriesResponse(BaseModel):
  stories: List[UserStory]