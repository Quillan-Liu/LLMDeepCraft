import json
from typing import Union, Tuple
from jsonschema import validate, ValidationError


def validate_json_str(
    input_data: Union[str, dict],
    valid_schema: dict
) -> Tuple[bool, str]:
  """
  验证用户故事JSON是否符合指定模式

  参数:
      input_data: 要验证的数据 (JSON字符串或字典)
      valid_schema: JSON Schema验证模式 (字典)

  返回:
      (验证结果, 错误信息)
  """
  try:
    if isinstance(input_data, str):
      data = json.loads(input_data)
    elif isinstance(input_data, dict):
      data = input_data
    else:
      return False, "输入必须是JSON字符串或字典"
  except json.JSONDecodeError as e:
    return False, f"无效的JSON格式: {str(e)}"

  try:
    if not isinstance(valid_schema, dict):
      return False, "验证模板必须是字典类型"

    validate(instance=data, schema=valid_schema)
    return True, "JSON 符合模板结构"

  except ValidationError as e:
    error_path = ".".join(
      map(str, e.absolute_path)) if e.absolute_path else "根对象"
    error_msg = f"字段 '{error_path}': {e.message}"
    return False, f"结构验证失败: {error_msg}"

  except Exception as e:
    return False, f"验证过程中发生意外错误: {str(e)}"


if __name__ == "__main__":
  from app.schemas.user_story_shemas import USER_STORY_VALIDATION_SCHEMA
  from app.schemas.data_entity_schemas import DATA_ENTITY_VALIDATION_SCHEMA

  user_story_test_str = """{
  "stories": [
    {
      "acceptance_criteria": [
        "Registration form accepts email and password",
        "System sends confirmation email upon registration",
        "User can log in with created credentials"
      ],
      "action": "I want to create an account",
      "role": "As a user",
      "value": "so that I can access the task management application"
    },
    {
      "acceptance_criteria": [
        "Login form accepts email and password",
        "Successful login redirects to dashboard",
        "Failed login shows appropriate error message"
      ],
      "action": "I want to log in to the application",
      "role": "As a user",
      "value": "so that I can access my projects and tasks"
    },
    {
      "acceptance_criteria": [
        "Project creation form includes name and description fields",
        "New project appears in my projects list",
        "Project is created with current user as owner"
      ],
      "action": "I want to create a new project",
      "role": "As a team member",
      "value": "so that I can organize related tasks together"
    },
    {
      "acceptance_criteria": [
        "Task creation form includes title and description",
        "Task is associated with selected project",
        "New task appears in project task list"
      ],
      "action": "I want to add tasks to a project",
      "role": "As a team member",
      "value": "so that I can break down work into manageable units"
    },
    {
      "acceptance_criteria": [
        "Task assignment shows list of available team members",
        "Assigned member receives notification",
        "Task shows assigned member in task details"
      ],
      "action": "I want to assign tasks to team members",
      "role": "As a team member",
      "value": "so that responsibilities are clearly distributed"
    },
    {
      "acceptance_criteria": [
        "Date picker allows selection of future dates",
        "Due date displays prominently on task card",
        "Overdue tasks are visually highlighted"
      ],
      "action": "I want to set due dates for tasks",
      "role": "As a team member",
      "value": "so that deadlines are clear and trackable"
    },
    {
      "acceptance_criteria": [
        "Complete button is visible on each task",
        "Completed tasks move to done section",
        "Progress metrics update immediately"
      ],
      "action": "I want to mark tasks as complete",
      "role": "As a team member",
      "value": "so that progress can be tracked accurately"
    },
    {
      "acceptance_criteria": [
        "Task changes appear instantly for all team members",
        "No page refresh required to see updates",
        "Online status of team members is visible"
      ],
      "action": "I want to see real-time updates",
      "role": "As a team member",
      "value": "so that I always have the latest project information"
    },
    {
      "acceptance_criteria": [
        "Invite form accepts email addresses",
        "Invited users receive email notification",
        "Accepted invitations add user to project team"
      ],
      "action": "I want to invite team members to projects",
      "role": "As a project manager",
      "value": "so that collaboration can begin quickly"
    },
    {
      "acceptance_criteria": [
        "Logout button is accessible from main navigation",
        "Session is terminated upon logout",
        "User is redirected to login page"
      ],
      "action": "I want to log out of the application",
      "role": "As a user",
      "value": "so that my account remains secure when not in use"
    }
  ]
}
"""

  print(validate_json_str(user_story_test_str, USER_STORY_VALIDATION_SCHEMA))

