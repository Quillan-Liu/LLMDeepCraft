from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class Cardinalities(str, Enum):
  OneToOne = "one_to_one"
  ManyToMany = "many_to_many"
  ManyToOne = "many_to_one"
  OneToMany = "one_to_many"


class EntityProperty(BaseModel):
  name: str = Field(description="Name of the field/column")
  label: str = Field(description="Label of the field/column")
  type: str = Field(description="Data type (e.g., string, integer, boolean)")
  length: int = Field(description="Length of the field/column")
  accuracy: int = Field(description="Accuracy of the field/column")
  required: bool = Field(description="Whether the field is required")
  description: Optional[str] = Field(
    description="Short description of what this field stores")
  is_primary_key: bool = Field(default=False,
                               description="Whether the field is a primary key")
  is_associated: bool = Field(default=False,
                              description="Whether the field is used for association")


class Relation(BaseModel):
  property: str = Field(description="Name of the property")
  related_property: str = Field(description="Name of the related property")


class EntityRelationship(BaseModel):
  entity: str = Field(description="Name of the entity")
  related_entity: str = Field(description="Name of the related entity")
  cardinality: Cardinalities = Field(
    description="Type of relation: OneToOne, OneToMany, ManyToMany, ManyToOne")
  relations: List[Relation] = Field(description="List of relations")


class EntityType(str, Enum):
  TYPE_TABLE = "table"
  TYPE_VIEW = "view"
  TYPE_LOGICAL = "logical"


class DataEntity(BaseModel):
  name: str = Field(description="Name of the entity (table name)")
  title: str = Field(description="Description of the entity (table title)")
  type: EntityType = Field(description="Type of the entity (table type)")
  properties: List[EntityProperty] = Field(description="List of properties")

