<div align="center">

# WhatShouldICite

**中文名：这段话该引谁**

</div>

> Suggest citations for selected text in your editor.

一个**编辑器内 Agent 形态**的科研辅助工具，帮助你在写作过程中快速判断是否需要引用，以及应该引用什么类型的工作。

## 🎯 核心特点

### 🌐 全局可用（已实现！）

- ✅ **跨应用使用**：在**任何应用**中都能使用（编辑器、浏览器、Word、WPS 等）
- ✅ **全局快捷键**：按下 `Ctrl + Shift + C` 即可触发
- ✅ **系统级浮窗**：不受应用限制，始终置顶显示

### 不打断写作流程

- ✅ **选中即用**：用鼠标选中一段文本，按下快捷键
- ✅ **即时反馈**：小浮窗立即显示引用建议
- ✅ **无需切换**：不复制粘贴，不切换窗口，不打断写作节奏

### 写作辅助 Agent

这不是一个文献生成器，而是一个**写作辅助 Agent**：

- 🤔 **帮你思考**：这段话是否需要引用？
- 🎯 **指引方向**：应该引用哪一类工作？
- 🔍 **提供线索**：推荐检索关键词

## 📋 输出格式

Agent 返回的内容适合在小浮窗中快速扫一眼：

```
【Do I need a citation?】
✔️ Yes / ⚠️ Optional / ❌ No

【Why】
- 简短一句话说明原因

【What to cite】
- Foundational works on XXX
- Recent methods for XXX
- Surveys on XXX（如适用）

【Search keywords】
- "xxx xxx problem"
- "xxx methods"
- "xxx benchmark"
```

**禁止输出：**
- ❌ 长段解释
- ❌ 学术废话
- ❌ 论文标题 / 作者名（Agent 不会编造引用）

## 🚀 快速开始

### 安装

```bash
pip install -r requirements.txt
pip install -e .
```

**注意**：Windows 上运行全局服务可能需要**管理员权限**（用于注册全局快捷键）。

### 🌐 全局使用（推荐）

**在任何应用中都能使用！**（编辑器、网页、WPS、Word 等）

```bash
python run_global_agent.py
```

启动后：
1. 在**任何应用**中选中一段文本
2. 按下 `Ctrl + Shift + C`（默认快捷键）
3. 立即看到浮窗中的引用建议
4. 按 `ESC` 关闭浮窗

**使用场景：**
- ✅ VS Code / Vim / 任何编辑器
- ✅ Chrome / Edge / 任何浏览器
- ✅ Word / WPS / 任何文档编辑器
- ✅ 任何可以选中文本的应用

### 📝 编程接口使用

```python
from whatshouldicite import CitationAgent

agent = CitationAgent()

# 分析选中文本
selected_text = "Deep learning has revolutionized computer vision in recent years."
result = agent.analyze(selected_text)
print(result)
```

### 命令行测试

```bash
python agent.py
```

## 📁 项目结构

```
whatshouldicite/
├── README.md
├── requirements.txt
├── agent.py               # Agent 命令行测试入口
├── whatshouldicite/
│   ├── __init__.py
│   ├── agent.py          # Agent 核心类（处理 selection）
│   ├── analyzer.py       # Text Analyzer
│   ├── intent.py         # Citation Intent Classifier
│   ├── planner.py         # Citation Type Planner
│   ├── keywords.py        # Keyword Generator
│   ├── prompts.py         # LLM 提示词模板
│   └── utils.py           # 工具函数
└── examples/
    └── agent_demo.md      # 使用示例
```

## 🔧 使用方式

### 方式 1：全局服务（推荐）

运行 `python run_global_agent.py`，即可在任何应用中：
- 选中文本 → 按快捷键 → **选择模式（1/2/3）** → 查看建议

**三种分析模式：**
- **模式 1**：规则判断（默认，快速免费）
- **模式 2**：LLM 判断（更准确，需要 API key）
- **模式 3**：混合模式（先规则，不确定时用 LLM）

**详见**：[MODE_SELECTION_GUIDE.md](MODE_SELECTION_GUIDE.md)

### 方式 2：编程接口

```python
from whatshouldicite import CitationAgent

agent = CitationAgent()
result = agent.analyze(selected_text)
```

### 方式 3：自定义快捷键

```python
from whatshouldicite.global_agent import GlobalCitationAgent

# 自定义快捷键
agent = GlobalCitationAgent(hotkey="ctrl+alt+c")
agent.start()
```

## 🧠 工作原理

Agent 包含以下逻辑模块：

1. **Text Analyzer**：分析文本特征（关键词、长度等）
2. **Citation Intent Classifier**：分类引用意图（方法、比较、事实陈述等）
3. **Citation Type Planner**：规划应该引用什么类型的工作
4. **Keyword Generator**：生成检索关键词

所有模块都满足：
- **输入** = 一小段被选中的文本（1–5 句话）
- **输出** = 可快速扫一眼的结构化说明

## ⚙️ LLM 集成（推荐！）

### ✅ 默认：规则判断（无需 API key）

**可以直接使用规则判断，完全免费！**

```python
from whatshouldicite import CitationAgent

# 直接使用，无需配置
agent = CitationAgent()  # 默认使用规则判断
result = agent.analyze("Deep learning has revolutionized computer vision.")
```

**优点：**
- ✅ **无需 API key**
- ✅ **无需网络连接**
- ✅ **完全免费**
- ✅ **快速响应**（毫秒级）
- ✅ **隐私安全**（完全本地处理）

**准确率**：约 70-80%（常见模式）

### 🤖 推荐：接入 LLM（准确率 85-95%）

**接入 LLM 后，准确率大幅提升！**

#### 快速开始（3 步）

1. **安装依赖**
```bash
pip install openai  # 或 anthropic
```

2. **配置 API key**
```bash
# 方式 1：环境变量
export OPENAI_API_KEY="sk-..."

# 方式 2：配置文件（推荐）
cp config_example.py config.py
# 编辑 config.py，填入 API key
```

3. **启动服务**
```bash
python run_with_llm.py
```

#### 编程方式

```python
from whatshouldicite import CitationAgent
from whatshouldicite.llm_client import OpenAIClient, UnifiedLLMClient

# OpenAI（推荐：GPT-3.5-turbo，便宜快速）
client = OpenAIClient(api_key="sk-...", model="gpt-3.5-turbo")
unified_client = UnifiedLLMClient(client)
agent = CitationAgent(llm_client=unified_client)

# 或 Anthropic Claude（推荐：Haiku，便宜快速）
from whatshouldicite.llm_client import AnthropicClient
client = AnthropicClient(api_key="sk-ant-...")
unified_client = UnifiedLLMClient(client)
agent = CitationAgent(llm_client=unified_client)
```

#### 成本

- **单次分析**：约 $0.0004（不到 0.001 元）
- **每天 100 次**：约 $0.04（约 0.3 元）
- **非常便宜！**

#### 支持的 LLM

- ✅ **OpenAI**：GPT-3.5-turbo（推荐）、GPT-4
- ✅ **Anthropic**：Claude Haiku（推荐）、Claude Sonnet、Claude Opus

**重要限制：**
- ✅ LLM 只用于：分类、推断、建议
- ❌ LLM **严禁**：编造引用、给出论文名称、给出作者

**详细指南**：
- 📖 [LLM_SETUP.md](LLM_SETUP.md) - 完整 LLM 配置指南
- 📖 [NO_API_KEY_NEEDED.md](NO_API_KEY_NEEDED.md) - 规则判断说明

## 🎯 设计目标

这个 Agent 的目标是：

- ✅ **不打断写作**：写作中途随时可召唤
- ✅ **不制造风险**：不编造引用，只给建议
- ✅ **不让用户思考"我该不该信它"**：明确这是建议，不是答案

而是：
> "哦，这里我应该去找某一类工作。"

## 📝 示例

查看 `examples/agent_demo.md` 了解详细使用示例。

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**记住**：这是一个**写作辅助 Agent**，而不是文献生成器。它帮助你思考，而不是替你思考。

