from langchain_core.prompts import ChatPromptTemplate

from app.work_flow.user_story.chain.prompts.user_stories_templates import USER_STORY_SCHEMA, \
    USER_STORY_SCHEMA_EXAMPLES


STORY_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
    # 用户故事生成协议

您是一位经验丰富的产品经理。请将原始需求转化为结构化的用户故事。

## 规则

1. 明确每个故事的功能名（用例名）

2. 每个故事必须遵循以下格式：“<功能名>：作为<角色>，我想要<操作>，以便<值>”。

3. 将复杂的需求分解为基本用户故事。

4. 包含必要的管理功能（登录、用户管理等）。

5. 每个用户故事提供 2-4 个清晰的验收标准。

6. 用户故事的 role 的json字符串的值应当使用汉字， "as a" 应当改为"作为" 

7. 功能名，用户故事的 action, value 以及 acceptance_criteria 的json字符串的值应当使用汉字

## 输出格式 (JSON)
{schema}

## 示例输出
{examples}""".format(
        schema=USER_STORY_SCHEMA,
        examples=USER_STORY_SCHEMA_EXAMPLES
    )),
    ("human", "User stories requirements: {user_stories_requirements}")
])


STORY_UPDATE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
        # 用户故事生成协议

    您是一位经验丰富的产品经理。请在给出的用户故事草稿和用户的改进要求下修改用户故事的草稿，然后将用户故事草稿和新增填的用户故事一起输出。
    
    ## 用户故事草稿
    
    {{user_stories_draft}}

    ## 规则

    1. 明确每个故事的功能名（用例名）

    2. 每个故事必须遵循以下格式：“<功能名>：作为<角色>，我想要<操作>，以便<值>”。

    3. 将复杂的需求分解为基本用户故事。

    4. 包含必要的管理功能（登录、用户管理等）。

    5. 每个用户故事提供 2-4 个清晰的验收标准。

    6. 用户故事的 role 的json字符串的值应当使用汉字， "as a" 应当改为"作为" 

    7. 功能名，用户故事的 action, value 以及 acceptance_criteria 的json字符串的值应当使用汉字

    ## 输出格式 (JSON)
    {schema}

    ## 示例输出
    {examples}""".format(
        schema=USER_STORY_SCHEMA,
        examples=USER_STORY_SCHEMA_EXAMPLES
    ).replace("{{user_stories_draft}}","{user_stories_draft}")),
    ("human", "User stories modification suggestions: {user_stories_modification_suggestions}")
])


JSON_TO_MD_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
你是一个专业的技术文档生成器。请将以下符合指定结构的 JSON 数据转换为清晰、结构良好、对人类友好的 Markdown 文档。严格遵循以下规则：

用户故事：
为每个用户故事的功能名使用一个四级标题（####），格式为“功能名：[function_name]”
为每个用户故事使用一个三级标题（###），格式为：“作为 [role]，我想要 [action]，以便 [value]”。
在每个故事下方，用无序列表列出验收标准（Acceptance Criteria），每条前加 -。
保持语言自然、简洁，避免技术术语堆砌。

要求：
1. 使用中文输出（除非原始数据中字段本身为英文专有名词，如 API 路径、字段名等）。
2. 不添加任何解释性前言或总结，直接输出 Markdown 内容。
3. 不修改、不推测、不补充原始 JSON 中未提供的信息。
4. 若某字段为空数组或 null，跳过该部分。
5. 格对齐美观，使用管道符格式。

markdown输出模版：

## 用户故事

### 功能名：[function_name]
### 作为 [role]，我想要 [action]，以便 [value]
- [验收标准 1]
- [验收标准 2]
...

markdown输出样例：

## 用户故事

### 功能名：订单提交
### 作为 客户，我想要 在线提交订单，以便 快速购买商品
- 订单必须包含至少一件商品
- 提交后应收到订单确认邮件

### 功能名：订单管理
### 作为 仓库管理员，我想要 查看待发货订单列表，以便 及时安排物流
- 列表按创建时间倒序排列
- 支持按订单状态筛选


现在，请基于上述规则，将 JSON 转换为 Markdown
"""
     ),
    ("human", """Result json:
{result_json}

将 result_json 转换为 Markdown
    """)
])

