# 🚀 LLM 快速开始（3 分钟）

## 为什么用 LLM？

规则判断准确率约 70-80%，LLM 判断准确率 85-95%，**显著提升！**

## 3 步开始

### 1️⃣ 安装依赖

```bash
pip install openai
# 或
pip install anthropic
```

### 2️⃣ 配置 API Key

**方式 A：环境变量（最简单）**

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key-here"

# Linux/Mac
export OPENAI_API_KEY="sk-your-key-here"
```

**方式 B：配置文件（推荐）**

```bash
# 复制配置模板
cp config_example.py config.py

# 编辑 config.py，填入你的 API key
# OPENAI_API_KEY = "sk-..."
```

**获取 API Key：**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/

### 3️⃣ 启动服务

```bash
python run_with_llm.py
```

**完成！** 现在在任何应用中选中文本，按 `Ctrl+Shift+C`，就能获得更智能的引用建议！

## 💰 成本

- **单次分析**：约 $0.0004（不到 0.001 元）
- **每天 100 次**：约 $0.04（约 0.3 元）
- **非常便宜！**

## 🎯 推荐配置

### 预算优先（推荐）

```python
# GPT-3.5-turbo：便宜快速，准确率 85%+
client = OpenAIClient(api_key="sk-...", model="gpt-3.5-turbo")
```

### 准确率优先

```python
# GPT-4：更准确，但稍贵
client = OpenAIClient(api_key="sk-...", model="gpt-4")
```

### 速度优先

```python
# Claude Haiku：最快，准确率也不错
client = AnthropicClient(api_key="sk-ant-...", model="claude-3-haiku-20240307")
```

## ❓ 常见问题

**Q: 必须用 LLM 吗？**
A: 不是！规则判断也能用，只是准确率稍低。

**Q: API key 安全吗？**
A: 只发送选中文本，不发送完整文档。建议设置 API key 使用限制。

**Q: 如果 API key 用完了？**
A: 程序会自动回退到规则判断，不影响使用。

**Q: 可以同时用多个 LLM 吗？**
A: 可以，但需要分别配置。建议选一个最适合的。

---

**详细文档**：[LLM_SETUP.md](LLM_SETUP.md)
