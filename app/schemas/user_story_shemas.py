from typing import List

from pydantic import BaseModel, Field


USER_STORY_SCHEMA = """
{{
  "stories": [
    {{
      "role": "As a [role]",
      "action": "I want [action]",
      "value": "so that [value]",
      "acceptance_criteria": [
        "Criterion 1",
        "Criterion 2"
      ]
    }}
  ]
}}
"""

USER_STORY_SCHEMA_EXAMPLES = """
{{
  "stories": [
    {{
      "role": "As a team member",
      "action": "I want to assign tasks to myself",
      "value": "so that I can track my responsibilities",
      "acceptance_criteria": [
        "Task assignment button is visible on task details",
        "Assigned task appears in my personal task list",
        "Notification is sent to me upon assignment"
      ]
    }},
    {{
      "role": "As a project manager",
      "action": "I want to view team progress reports",
      "value": "so that I can identify bottlenecks",
      "acceptance_criteria": [
        "Reports show tasks by status (todo, in progress, done)",
        "Data updates within 5 minutes of task change",
        "Export to CSV option available"
      ]
    }}
  ]
}}
"""

USER_STORY_VALIDATION_SCHEMA = {
    "type": "object",
    "properties": {
        "stories": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "role": {"type": "string"},
                    "action": {"type": "string"},
                    "value": {"type": "string"},
                    "acceptance_criteria": {
                        "type": "array",
                        "minItems": 1,
                        "items": {"type": "string"}
                    }
                },
                "required": ["role", "action", "value", "acceptance_criteria"],
                "additionalProperties": False
            }
        }
    },
    "required": ["stories"],
    "additionalProperties": False
}


class UserStory(BaseModel):
  role: str = Field(description="The actor in the story (e.g., User, Admin)")
  action: str = Field(description="What the actor wants to do")
  value: str = Field(description="The benefit or value of the action")
  acceptance_criteria: List[str] = Field(
    description="List of criteria to verify the story is done")


class UserStoriesResponse(BaseModel):
  stories: List[UserStory]