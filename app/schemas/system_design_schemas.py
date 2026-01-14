from typing import List

from pydantic import BaseModel, Field


class APIEndpoint(BaseModel):
  method: str = Field(description="HTTP Method (GET, POST, PUT, DELETE)")
  path: str = Field(description="API Path (e.g., /api/users)")
  summary: str = Field(description="Short summary of what the endpoint does")


class SystemModule(BaseModel):
  name: str = Field(
    description="Name of the module (e.g., Auth, Order, Payment)")
  description: str = Field(
    description="High-level description of the module's responsibility")
  key_features: List[str] = Field(
    description="List of key features in this module")
  api_endpoints: List[APIEndpoint] = Field(
    description="Proposed API endpoints for this module")


class SystemDesignResponse(BaseModel):
  modules: List[SystemModule]
