import json


def generate_data_model_data(data_model_dict: dict) -> str:
  return json.dumps(
      {
        "data_model_response": {
          "entities": [
            {
              "name": entity["name"],
              "title": entity["title"],
              "type": entity["type"].value,
              "properties": [
                {
                  "name": prop["name"],
                  "label": prop["label"],
                  "type": prop["type"],
                  "length": prop["length"],
                  "accuracy": prop["accuracy"],
                  "required": prop["required"],
                  "description": prop["description"],
                  "is_primary_key": prop["is_primary_key"],
                  "is_associated": prop["is_associated"]
                }
                for prop in entity["properties"]
              ]
            }
            for entity in data_model_dict["entities"]
          ],
          "relationships": [
            {
              "entity": rel["entity"],
              "related_entity": rel["related_entity"],
              "cardinality": rel["cardinality"].value,
              "relations": [
                {
                  "property": r["property"],
                  "related_property": r["related_property"]
                }
                for r in rel["relations"]
              ]
            }
            for rel in data_model_dict["relationships"]
          ]
        }
      },
      indent=2
  )