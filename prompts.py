"""
提示词模板 - 用于 LLM 分析选中文本的引用需求
"""

ANALYZE_PROMPT = """你是一个科研写作助手。分析以下选中的文本，判断是否需要引用。

选中文本：
{selected_text}

请按照以下格式输出：

【Do I need a citation?】
Yes / Optional / No

【Why】
- 简短一句话说明原因（不超过50字）

【What to cite】（如果需要引用）
- Foundational works on XXX
- Recent methods for XXX
- Surveys on XXX（如适用）

【Search keywords】（如果需要引用）
- "keyword1 keyword2"
- "keyword3 keyword4"

重要要求：
- 只做分类和推断，不要编造具体的论文标题或作者名
- 输出必须严格按照上述格式
- 如果不需要引用，只输出前两部分即可
"""

INTENT_CLASSIFY_PROMPT = """判断以下文本的引用意图类型：

文本：{text}

可能的类型：
- Factual claim（事实性陈述）
- Method/Technique（方法技术）
- Comparison（比较）
- Survey/Review（综述）
- Foundational work（基础性工作）
- Recent advance（最新进展）
- Common knowledge（常识，不需要引用）

只返回类型名称，不要其他解释。"""

PLANNER_PROMPT = """基于以下文本和引用意图，规划应该引用什么类型的工作：

文本：{text}
引用意图：{intent}

输出格式：
- Foundational works on XXX
- Recent methods for XXX
- Surveys on XXX（如适用）

只输出引用类型建议，不要具体论文名。"""

KEYWORD_PROMPT = """为以下文本生成3-5个检索关键词，用于查找相关引用：

文本：{text}
引用类型：{citation_type}

要求：
- 关键词应该是学术搜索中常用的术语
- 格式："keyword1 keyword2"
- 每个关键词一行

只输出关键词，不要其他解释。"""
