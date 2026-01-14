from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

DATA_ENTITY_SCHEMA = """
{{
  "data_model_response": {{
    "entities": [
      {{
        "name": "<entity_name>",
        "title": "<entity_description>",
        "type": "<table|view|logical>",
        "properties": [
          {{
            "name": "<column_name>",
            "label": "<human_readable_label>",
            "type": "<data_type>",
            "length": <max_length>,
            "accuracy": <decimal_precision>,
            "required": <true|false>,
            "description": "<optional_field_description>",
            "is_primary_key": <true|false>,
            "is_associated": <true|false>
          }}
        ]
      }}
    ],
    "relationships": [
      {{
        "entity": "<source_entity_name>",
        "related_entity": "<target_entity_name>",
        "cardinality": "<one_to_one|many_to_many|many_to_one|one_to_many>",
        "relations": [
          {{
            "property": "<source_property>",
            "related_property": "<target_property>"
          }}
        ]
      }}
    ]
  }}
}}
"""

DATA_ENTITY_SCHEMA_EXAMPLES = """
{{
  "data_model_response": {{
    "entities": [
      {{
        "name": "customers",
        "title": "Customer master data",
        "type": "table",
        "properties": [
          {{
            "name": "customer_id",
            "label": "Customer ID",
            "type": "integer",
            "length": 0,
            "accuracy": 0,
            "required": true,
            "description": "Unique customer identifier",
            "is_primary_key": true,
            "is_associated": false
          }},
          {{
            "name": "email",
            "label": "Email Address",
            "type": "string",
            "length": 255,
            "accuracy": 0,
            "required": true,
            "description": "Primary contact email",
            "is_primary_key": false,
            "is_associated": false
          }}
        ]
      }},
      {{
        "name": "orders",
        "title": "Customer orders",
        "type": "table",
        "properties": [
          {{
            "name": "order_id",
            "label": "Order ID",
            "type": "string",
            "length": 36,
            "accuracy": 0,
            "required": true,
            "description": "UUID for order tracking",
            "is_primary_key": true,
            "is_associated": false
          }},
          {{
            "name": "customer_id",
            "label": "Customer Reference",
            "type": "integer",
            "length": 0,
            "accuracy": 0,
            "required": true,
            "description": "Foreign key to customers",
            "is_primary_key": false,
            "is_associated": true
          }}
        ]
      }}
    ],
    "relationships": [
      {{
        "entity": "customers",
        "related_entity": "orders",
        "cardinality": "one_to_many",
        "relations": [
          {{
            "property": "customer_id",
            "related_property": "customer_id"
          }}
        ]
      }}
    ]
  }}
}}
"""

DATA_ENTITY_VALIDATION_SCHEMA = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DataModelResponseValidation",
  "type": "object",
  "properties": {
    "data_model_response": {
      "type": "object",
      "required": ["entities", "relationships"],
      "properties": {
        "entities": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "title", "type", "properties"],
            "properties": {
              "name": {"type": "string"},
              "title": {"type": "string"},
              "type": {"enum": ["table", "view", "logical"]},
              "properties": {
                "type": "array",
                "items": {
                  "type": "object",
                  "required": [
                    "name", "label", "type", "length", "accuracy", 
                    "required", "is_primary_key", "is_associated"
                  ],
                  "properties": {
                    "name": {"type": "string"},
                    "label": {"type": "string"},
                    "type": {"type": "string"},
                    "length": {"type": "integer", "minimum": 0},
                    "accuracy": {"type": "integer", "minimum": 0},
                    "required": {"type": "boolean"},
                    "description": {"type": ["string", "null"]},
                    "is_primary_key": {"type": "boolean"},
                    "is_associated": {"type": "boolean"}
                  }
                }
              }
            }
          }
        },
        "relationships": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["entity", "related_entity", "cardinality", "relations"],
            "properties": {
              "entity": {"type": "string"},
              "related_entity": {"type": "string"},
              "cardinality": {
                "enum": ["one_to_one", "many_to_many", "many_to_one", "one_to_many"]
              },
              "relations": {
                "type": "array",
                "items": {
                  "type": "object",
                  "required": ["property", "related_property"],
                  "properties": {
                    "property": {"type": "string"},
                    "related_property": {"type": "string"}
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "required": ["data_model_response"]
}


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


class DataModelResponse(BaseModel):
  entities: List[DataEntity]
  relationships: List[EntityRelationship]
