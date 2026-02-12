# 🤖 LLM 集成使用指南

## 为什么需要 LLM？

规则判断虽然快速免费，但准确率有限（约 70-80%）。接入 LLM 后：
- ✅ **准确率提升**：85-95%
- ✅ **理解上下文**：能理解复杂语义
- ✅ **更智能的建议**：更精准的引用类型和关键词

## 🚀 快速开始

### 方式 1：使用配置文件（推荐）

1. **复制配置模板**
```bash
cp config_example.py config.py
```

2. **编辑 config.py，填入你的 API key**
```python
OPENAI_API_KEY = "sk-..."  # 你的 OpenAI API key
# 或
ANTHROPIC_API_KEY = "sk-ant-..."  # 你的 Anthropic API key
```

3. **启动服务**
```bash
python run_with_llm.py
```

### 方式 2：使用环境变量

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-..."
python run_with_llm.py

# Linux/Mac
export OPENAI_API_KEY="sk-..."
python run_with_llm.py
```

### 方式 3：编程方式

```python
from whatshouldicite import CitationAgent
from whatshouldicite.llm_client import OpenAIClient, UnifiedLLMClient

# OpenAI
client = OpenAIClient(api_key="sk-...", model="gpt-3.5-turbo")
unified_client = UnifiedLLMClient(client)
agent = CitationAgent(llm_client=unified_client)

# 或 Anthropic
from whatshouldicite.llm_client import AnthropicClient
client = AnthropicClient(api_key="sk-ant-...", model="claude-3-haiku-20240307")
unified_client = UnifiedLLMClient(client)
agent = CitationAgent(llm_client=unified_client)
```

## 📋 支持的 LLM

### OpenAI

- **模型**：`gpt-3.5-turbo`（推荐，便宜快速）、`gpt-4`、`gpt-4-turbo-preview`
- **获取 API Key**：https://platform.openai.com/api-keys
- **价格**：GPT-3.5-turbo 约 $0.0015/1K tokens（非常便宜）

```python
from whatshouldicite.llm_client import OpenAIClient, UnifiedLLMClient

client = OpenAIClient(api_key="sk-...", model="gpt-3.5-turbo")
unified_client = UnifiedLLMClient(client)
```

### Anthropic Claude

- **模型**：`claude-3-haiku-20240307`（推荐，便宜快速）、`claude-3-sonnet-20240229`、`claude-3-opus-20240229`
- **获取 API Key**：https://console.anthropic.com/
- **价格**：Claude Haiku 约 $0.25/1M tokens（非常便宜）

```python
from whatshouldicite.llm_client import AnthropicClient, UnifiedLLMClient

client = AnthropicClient(api_key="sk-ant-...", model="claude-3-haiku-20240307")
unified_client = UnifiedLLMClient(client)
```

## 💰 成本估算

### 单次分析成本（GPT-3.5-turbo）

- **输入**：约 100 tokens（选中文本 + 提示词）
- **输出**：约 150 tokens（分析结果）
- **总成本**：约 $0.0004（不到 0.001 元人民币）

**每天使用 100 次**：约 $0.04（约 0.3 元人民币）

### 单次分析成本（Claude Haiku）

- **输入**：约 100 tokens
- **输出**：约 150 tokens
- **总成本**：约 $0.00006（不到 0.0005 元人民币）

**每天使用 100 次**：约 $0.006（约 0.04 元人民币）

**结论**：成本非常低，可以放心使用！

## 🔧 配置助手

运行配置助手，交互式设置：

```bash
python setup_llm.py
```

## ⚙️ 高级配置

### 自定义模型参数

```python
from whatshouldicite.llm_client import OpenAIClient, UnifiedLLMClient

client = OpenAIClient(
    api_key="sk-...",
    model="gpt-4"  # 使用 GPT-4
)

unified_client = UnifiedLLMClient(client)
agent = CitationAgent(llm_client=unified_client)
```

### 混合模式（规则 + LLM）

可以设置只在不确定时使用 LLM：

```python
# 先尝试规则判断
agent = CitationAgent()  # 规则判断
result = agent.analyze(text)

# 如果结果不确定，再用 LLM
if "Optional" in result:
    llm_agent = CitationAgent(llm_client=unified_client)
    result = llm_agent.analyze(text)
```

## 🐛 故障排除

### 问题 1：API Key 无效

**症状**：`API 调用失败: Invalid API key`

**解决**：
- 检查 API key 是否正确
- 确认 API key 有足够的余额
- OpenAI：检查 https://platform.openai.com/account/usage
- Anthropic：检查 https://console.anthropic.com/settings/usage

### 问题 2：网络连接失败

**症状**：`API 调用失败: Connection error`

**解决**：
- 检查网络连接
- 如果在中国大陆，可能需要代理
- 设置代理：`export HTTPS_PROXY="http://127.0.0.1:7890"`

### 问题 3：超出速率限制

**症状**：`API 调用失败: Rate limit exceeded`

**解决**：
- 降低使用频率
- 升级 API 套餐
- 使用更便宜的模型（如 GPT-3.5-turbo）

### 问题 4：LLM 分析失败，回退到规则

**症状**：看到 "LLM 分析失败，使用规则判断"

**解决**：
- 检查 API key 和网络
- 查看错误信息
- 程序会自动回退到规则判断，不影响使用

## 📊 规则判断 vs LLM 判断对比

| 特性 | 规则判断 | LLM 判断 |
|------|---------|---------|
| 准确率 | 70-80% | 85-95% |
| 速度 | 毫秒级 | 1-3 秒 |
| 成本 | 免费 | 极低（$0.0004/次） |
| 需要网络 | ❌ | ✅ |
| 需要 API key | ❌ | ✅ |
| 理解上下文 | 弱 | 强 |

## 💡 建议

- **日常使用**：GPT-3.5-turbo 或 Claude Haiku（便宜快速）
- **重要论文**：GPT-4 或 Claude Opus（更准确）
- **预算有限**：规则判断 + 重要部分用 LLM
- **追求速度**：规则判断（毫秒级）

## 🔒 隐私和安全

- ✅ API 调用只发送选中文本，不发送完整文档
- ✅ 不存储任何数据
- ✅ 可以设置 API key 使用限制
- ⚠️ 选中文本会发送到 LLM 服务商（OpenAI/Anthropic）

---

**现在就开始使用 LLM，获得更智能的引用建议！** 🚀
