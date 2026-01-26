from pydantic import BaseModel

from app.logger.logger import logger


def base_model_to_json(model: BaseModel) -> str:
  if not isinstance(model, BaseModel):
    raise TypeError("输入的模型必须是BaseModel")

  json_str = model.model_dump_json()

  return json_str

def base_model_to_dict(model: BaseModel) -> dict:
  if not isinstance(model, BaseModel):
    logger.error("输入的模型不是 BaseModel")
    raise TypeError("输入的模型必须是 BaseModel")

  json_dict = model.model_dump()

  return json_dict


if __name__ == '__main__':
  import json
  from datetime import datetime
  from typing import List, Optional, Union


  def are_json_equal(json_str1: str, json_str2: str) -> bool:
    try:
      json1 = json.loads(json_str1)
      json2 = json.loads(json_str2)
      return json1 == json2

    except json.decoder.JSONDecodeError:
      raise TypeError("必须同时输入两个json字符串")

  class Address(BaseModel):
    city: str
    zip_code: str


  class User(BaseModel):
    id: int
    name: str
    created_at: datetime
    address: Address
    tags: List[str] = []
    friend: Optional['User'] = None


  address = Address(city="New York", zip_code="10001")
  user = User(
      id=1,
      name="Alice",
      created_at=datetime(2023, 1, 1, 12, 0),
      address=address,
      tags=["admin", "premium"]
  )

  target_str = """
  {
    "id": 1,
    "name": "Alice",
    "created_at": "2023-01-01T12:00:00",
    "address": {
      "city": "New York",
      "zip_code": "10001"
    },
    "tags": [
      "admin",
      "premium"
    ],
    "friend": null
  }
  """
  assert are_json_equal(target_str, base_model_to_json(user))
