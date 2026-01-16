from langchain_core.prompts import ChatPromptTemplate
from app.schemas.user_story_shemas import USER_STORY_SCHEMA, USER_STORY_SCHEMA_EXAMPLES
from app.schemas.data_entity_schemas import DATA_ENTITY_SCHEMA, DATA_ENTITY_SCHEMA_EXAMPLES

# 1. User Story Prompt
STORY_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """# 用户故事生成协议

您是一位经验丰富的产品经理。请将原始需求转化为结构化的用户故事。

## 规则

1. 每个故事必须遵循以下格式：“作为<角色>，我想要<操作>，以便<值>”。

2. 将复杂的需求分解为基本用户故事。

3. 包含必要的管理功能（登录、用户管理等）。

4. 每个用户故事提供 2-4 个清晰的验收标准。

5. 用户故事的 role 的json字符串的值应当使用汉字， "as a" 应当改为"作为" 

6. 用户故事的 action, value 以及 acceptance_criteria 的json字符串的值应当使用汉字

## 输出格式 (JSON)
{schema}

## 示例输出
{examples}""".format(
        schema=USER_STORY_SCHEMA,
        examples=USER_STORY_SCHEMA_EXAMPLES
    )),
    ("human", "Raw Requirements: {raw_requirements}")
])


# 2. Data Modeling Prompt
DATA_MODELING_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """您是一位资深的数据库架构师。

您的目标是根据提供的用户故事设计一个健壮的数据模型（ER图）。

请遵循以下规则：

1. 从用户故事中识别所有必要的名词/实体。

2. 定义具有适当数据类型的字段。

3. 确定实体之间的关系（1:1、1:N、N:M）。

4. 规范化数据库设计（至少达到3NF）。

5. 确保命名约定一致（字段使用蛇形命名法，实体使用帕斯卡命名法）。

6. 说明或描述的内容应当使用中文。

输出必须是符合DataModelResponse模式的有效JSON对象。

## 输出格式（JSON）
{schema}

## 示例输出
{examples}""".format(
        schema=DATA_ENTITY_SCHEMA,
        examples=DATA_ENTITY_SCHEMA_EXAMPLES
    )),
    ("human", """User Stories:
{user_stories}

根据这些故事，生成数据模型。
""")
])

# 3. System Design Prompt
SYSTEM_DESIGN_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """您是一位经验丰富的软件架构师。

您的目标是根据用户故事和数据模型设计系统模块和 API 定义。

请遵循以下规则：

1. 将相关功能分组到内聚模块中（例如，身份验证、库存管理、订单管理）。

2. 为每个模块定义关键的 RESTful API 端点。

3. 确保设计符合用户故事中定义的需求。

4. 使用标准的 HTTP 方法（GET、POST、PUT、DELETE）。

5. 说明或描述的内容应当使用中文

输出必须是符合 SystemDesignResponse 架构的有效 JSON 对象。
"""),
    ("human", """User Stories:
{user_stories}

Data Model:
{data_model}

基于以上内容，生成系统设计模块。""")
])
