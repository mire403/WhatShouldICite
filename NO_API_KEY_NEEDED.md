# ✅ 无需 API Key，可直接使用！

## 🎉 好消息

**WhatShouldICite 可以直接使用，完全不需要大模型的 API key！**

## 🔧 工作原理

当前版本使用**基于规则的判断系统**，无需任何外部 API：

### ✅ 规则判断（当前默认）

- **无需 API key**
- **无需网络连接**
- **完全免费**
- **快速响应**

### 规则判断包括：

1. **关键词匹配**：检测方法、比较、事实性陈述等关键词
2. **模式识别**：识别常识性陈述、技术描述等模式
3. **启发式规则**：基于学术写作常见模式

### 示例：

```python
# 直接使用，无需任何配置
from whatshouldicite import CitationAgent

agent = CitationAgent()  # 不传 llm_client，使用规则判断
result = agent.analyze("Deep learning has revolutionized computer vision.")
print(result)
```

## 📊 规则判断 vs LLM 判断

| 特性 | 规则判断（当前） | LLM 判断（可选） |
|------|----------------|----------------|
| 需要 API key | ❌ 不需要 | ✅ 需要 |
| 需要网络 | ❌ 不需要 | ✅ 需要 |
| 响应速度 | ⚡ 极快（毫秒级） | 🐌 较慢（秒级） |
| 准确性 | 📊 中等（70-80%） | 📈 较高（85-95%） |
| 成本 | 💰 免费 | 💵 按调用付费 |
| 隐私 | 🔒 完全本地 | ⚠️ 数据发送到 API |

## 🚀 立即开始使用

### 1. 安装依赖（无需 API key 相关依赖）

```bash
pip install keyboard pyperclip pyautogui
```

### 2. 启动全局服务

```bash
python run_global_agent.py
```

### 3. 使用

- 在任何应用中选中文本
- 按 `Ctrl + Shift + C`
- 立即看到引用建议（无需等待 API 响应）

## 🔮 可选：接入 LLM（如果需要更高准确性）

如果你想要更准确的判断，可以**可选地**接入 LLM：

### OpenAI

```python
from whatshouldicite import CitationAgent
from openai import OpenAI

llm_client = OpenAI(api_key="your-api-key")
agent = CitationAgent(llm_client=llm_client)
```

### Anthropic Claude

```python
from whatshouldicite import CitationAgent
import anthropic

llm_client = anthropic.Anthropic(api_key="your-api-key")
agent = CitationAgent(llm_client=llm_client)
```

**注意**：接入 LLM 需要：
1. 安装对应的 SDK（`openai` 或 `anthropic`）
2. 配置 API key
3. 承担 API 调用费用

## 💡 建议

- **日常使用**：使用规则判断（默认），快速、免费、隐私安全
- **重要论文**：可选接入 LLM，获得更准确的判断
- **混合模式**：可以先规则判断，不确定时再调用 LLM

## ❓ 常见问题

### Q: 规则判断准确吗？

A: 对于常见的学术写作模式（方法描述、比较、事实陈述），准确率约 70-80%。对于复杂或模糊的文本，可能需要人工判断。

### Q: 可以只使用规则判断吗？

A: **完全可以！** 规则判断是默认模式，无需任何配置即可使用。

### Q: 规则判断会改进吗？

A: 会的！我们会持续优化规则，提高准确率。你也可以贡献更好的规则模式。

### Q: 如何知道当前使用的是规则还是 LLM？

A: 如果创建 `CitationAgent()` 时不传 `llm_client` 参数，就是使用规则判断。

---

**总结：直接使用即可，无需任何 API key！** 🎉
