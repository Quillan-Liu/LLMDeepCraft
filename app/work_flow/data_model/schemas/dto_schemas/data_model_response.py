from enum import Enum
from typing import List

from pydantic import BaseModel

from app.work_flow.data_model.schemas.domain_schemas.data_model_domains import \
  DataEntity, EntityRelationship


class DataModelResponse(BaseModel):
  entities: List[DataEntity]
  relationships: List[EntityRelationship]