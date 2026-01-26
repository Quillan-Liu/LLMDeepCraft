from langchain_core.prompts import ChatPromptTemplate

from app.work_flow.data_model.chain.prompts.data_model_templates import \
  DATA_ENTITY_SCHEMA, DATA_ENTITY_SCHEMA_EXAMPLES

DATA_MODEL_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """您是一位资深的数据库架构师。

您的目标是根据提供的用户故事设计一个健壮的数据模型（ER图）。

请遵循以下规则：

1. 从用户故事中识别所有必要的名词/实体。

2. 定义具有适当数据类型的字段。

3. 确定实体之间的关系（1:1、1:N、N:M）。

4. 规范化数据库设计（至少达到3NF）。

5. 确保命名约定一致（字段使用蛇形命名法，实体使用帕斯卡命名法）。

6. 说明或描述的内容应当使用中文。

## 用户故事
{{user_story_result}}

输出必须是符合DataModelResponse模式的有效JSON对象。

## 输出格式（JSON）
{schema}

## 示例输出
{examples}""".format(
        schema=DATA_ENTITY_SCHEMA,
        examples=DATA_ENTITY_SCHEMA_EXAMPLES
    ).replace("{{user_story_result}}", "{user_story_result}")),
    ("human", """User Requirements:
{user_requirements}

根据这些故事，生成数据模型。
""")
])


DATA_MODEL_MODIFICATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """您是一位资深的数据库架构师。

您的目标是根据提供的用户故事以及用户的自然语言需求修改数据模型草稿。

请遵循以下规则：

1. 从用户故事中识别所有必要的名词/实体。

2. 定义具有适当数据类型的字段。

3. 确定实体之间的关系（1:1、1:N、N:M）。

4. 规范化数据库设计（至少达到3NF）。

5. 确保命名约定一致（字段使用蛇形命名法，实体使用帕斯卡命名法）。

6. 说明或描述的内容应当使用中文。

## 用户故事
{{user_story_result}}

## 数据模型草稿
{{data_model_draft}}

输出必须是符合DataModelResponse模式的有效JSON对象。

## 输出格式（JSON）
{schema}

## 示例输出
{examples}""".format(
        schema=DATA_ENTITY_SCHEMA,
        examples=DATA_ENTITY_SCHEMA_EXAMPLES
    ).replace("{{user_story_result}}", "{user_story_result}")
     .replace("{{data_model_draft}}", "{data_model_draft}")),
    ("human", """User Requirements:
{user_requirements}

根据这些故事，生成数据模型。
""")
])


JSON_TO_MD_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
你是一个专业的技术文档生成器。请将以下符合指定结构的 JSON 数据转换为清晰、结构良好、对人类友好的 Markdown 文档。严格遵循以下规则：

数据模型：
先列出所有实体（Entities），每个实体使用四级标题（####）显示其 title（若无 title 则用 name）。
在每个实体下，用表格展示其属性（properties），表头为：| 字段名 | 标签 | 类型 | 长度 | 精度 | 必填 | 主键 | 关联字段 | 描述 |
“长度”仅当 length > 0 时显示数值，否则留空。
“精度”仅当 accuracy > 0 时显示数值，否则留空。
“主键”和“关联字段”列用 True 表示 true，False 表示 false。
然后列出实体间关系（Relationships）：
每个关系用一段文字描述，格式为：“[entity] 与 [related_entity] 之间是 [cardinality] 关系。”
若存在具体关联字段（relations），追加说明：“通过 [property] ↔ [related_property] 关联。”

要求：
1. 使用中文输出（除非原始数据中字段本身为英文专有名词，如 API 路径、字段名等）。
2. 不添加任何解释性前言或总结，直接输出 Markdown 内容。
3. 不修改、不推测、不补充原始 JSON 中未提供的信息。
4. 若某字段为空数组或 null，跳过该部分（如无 relationships，则不显示关系段落）。
5. 格对齐美观，使用管道符格式。


markdown输出模版：

### 数据模型

#### [实体标题或名称]

| 字段名 | 标签 | 类型 | 长度 | 精度 | 必填 | 主键 | 关联字段 | 描述 |
|--------|------|------|------|------|------|------|----------|------|
| ...    | ...  | ...  | ...  | ...  | True/False  | True/False  | True/False  | ...  |

（可选）  
`[实体A]` 与 `[实体B]` 之间是 `[cardinality]` 关系。通过 `[property]` ↔ `[related_property]` 关联。


markdown输出样例：

### 数据模型

#### 用户

| 字段名 | 标签 | 类型 | 长度 | 精度 | 必填 | 主键 | 关联字段 | 描述 |
|--------|------|------|------|------|------|------|----------|------|
| id | 用户ID | integer |  |  | True | True | False | 系统唯一标识 |
| email | 邮箱 | string | 255 |  | True | False | False | 登录账号，唯一 |
| created_at | 注册时间 | datetime |  |  | True | False | False | 账号创建时间 |

#### 订单

| 字段名 | 标签 | 类型 | 长度 | 精度 | 必填 | 主键 | 关联字段 | 描述 |
|--------|------|------|------|------|------|------|----------|------|
| order_id | 订单编号 | string | 36 |  | True | True | False | UUID格式 |
| user_id | 用户ID | integer |  |  | True | False | True | 关联用户主键 |
| status | 订单状态 | string | 20 |  | True | False | False | 如：pending, shipped |
| total_amount | 总金额 | decimal |  | 2 | True | False | False | 精确到分 |

### 商品

| 字段名 | 标签 | 类型 | 长度 | 精度 | 必填 | 主键 | 关联字段 | 描述 |
|--------|------|------|------|------|------|------|----------|------|
| product_id | 商品ID | integer |  |  | True | True | False | 自增主键 |
| name | 商品名称 | string | 100 |  | True | False | False | 展示名称 |
| price | 单价 | decimal |  | 2 | True | False | False | 单位：元 |

订单 与 用户 之间是 one_to_many 关系。通过 user_id ↔ id 关联。


现在，请基于上述规则，将 JSON 转换为 Markdown
"""
     ),
    ("human", """Result json:
{result_json}

将 result_json 转换为 Markdown
    """)
])
