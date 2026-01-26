USER_STORY_SCHEMA = """
{{
  "stories": [
    {{
      "function_name": "[function_name]",
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
      "function_name": "任务分配及追踪",
      "role": "作为团队成员",
      "action": "我想给自己分配任务",
      "value": "这样我就可以追踪我的职责",
      "acceptance_criteria": [
        "任务分配按钮显示在任务详情中",
        "分配的任务会出现在我的个人任务列表中"
        "任务分配完成后，我会收到通知"
      ]
    }},
    {{
      "function_name": "任务进度检测及分析",
      "role": "作为项目经理",
      "action": "我想查看团队进度报告",
      "value": "这样我就可以找出瓶颈",
      "acceptance_criteria": [
        "报告按状态（待办、进行中、已完成）显示任务",
        "任务变更后 5 分钟内更新数据",
        "提供导出为 CSV 的选项"
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
                "required": ["function_name", "role", "action", "value", "acceptance_criteria"],
                "additionalProperties": False
            }
        }
    },
    "required": ["stories"],
    "additionalProperties": False
}