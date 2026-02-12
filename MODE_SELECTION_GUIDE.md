# 🎯 模式选择功能使用指南

## 功能概述

现在支持**三种分析模式**，用户可以在每次分析时选择：

1. **规则判断**（默认）- 快速、免费、无需 API key
2. **LLM 判断** - 更准确，需要 API key
3. **混合模式** - 先规则判断，不确定时用 LLM

## 🚀 使用方法

### 基本流程

1. **在任何应用中选中文本**
2. **按下快捷键** `Ctrl + Shift + C`
3. **选择分析模式**（按 1/2/3 键）
   - 按 `1` - 规则判断（默认）
   - 按 `2` - LLM 判断
   - 按 `3` - 混合模式
4. **查看引用建议浮窗**
5. **按 `ESC` 关闭浮窗**

### 模式选择窗口

按下快捷键后，会弹出模式选择窗口：

```
┌─────────────────────────────────────┐
│      选择分析模式                    │
├─────────────────────────────────────┤
│ [1] 规则判断（默认）                 │
│     快速、免费、无需 API key         │
│     准确率：70-80%                   │
│                                     │
│ [2] LLM 判断                        │
│     更准确、需要 API key             │
│     准确率：85-95%                   │
│                                     │
│ [3] 混合模式                        │
│     先规则判断，不确定时用 LLM       │
│     平衡速度和准确率                │
└─────────────────────────────────────┘
```

## 📊 三种模式对比

| 特性 | 规则判断 | LLM 判断 | 混合模式 |
|------|---------|---------|---------|
| **速度** | ⚡ 毫秒级 | 🐌 1-3 秒 | ⚡ 通常毫秒级 |
| **准确率** | 70-80% | 85-95% | 80-90% |
| **成本** | 💰 免费 | 💵 极低 | 💰 通常免费 |
| **需要 API key** | ❌ | ✅ | ✅（可选） |
| **适用场景** | 日常使用 | 重要论文 | 平衡需求 |

## 🎯 模式选择建议

### 选择规则判断（模式 1）当：
- ✅ 快速判断，不需要最高准确率
- ✅ 没有配置 API key
- ✅ 日常写作，常见模式
- ✅ 预算有限

### 选择 LLM 判断（模式 2）当：
- ✅ 重要论文，需要高准确率
- ✅ 复杂或模糊的文本
- ✅ 已配置 API key
- ✅ 愿意等待 1-3 秒

### 选择混合模式（模式 3）当：
- ✅ 想要平衡速度和准确率
- ✅ 已配置 API key
- ✅ 大部分文本用规则判断，不确定时用 LLM
- ✅ 节省 API 调用成本

## 🔧 配置 LLM（可选）

如果要使用 LLM 判断或混合模式，需要配置 API key：

### 方式 1：环境变量

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-..."

# Linux/Mac
export OPENAI_API_KEY="sk-..."
```

### 方式 2：配置文件

```bash
# 复制配置模板
cp config_example.py config.py

# 编辑 config.py，填入 API key
OPENAI_API_KEY = "sk-..."
```

### 方式 3：启动时自动检测

运行 `python run_with_llm.py`，程序会自动检测配置的 API key。

## 📝 使用示例

### 示例 1：日常使用（规则判断）

1. 选中文本："Deep learning has revolutionized computer vision."
2. 按 `Ctrl + Shift + C`
3. 按 `1`（规则判断）
4. 立即看到建议（毫秒级）

### 示例 2：重要论文（LLM 判断）

1. 选中文本："Our novel approach combines transformer architecture with reinforcement learning..."
2. 按 `Ctrl + Shift + C`
3. 按 `2`（LLM 判断）
4. 等待 1-3 秒，看到更准确的建议

### 示例 3：平衡使用（混合模式）

1. 选中文本："Recent studies show improvements..."
2. 按 `Ctrl + Shift + C`
3. 按 `3`（混合模式）
4. 先用规则判断（快速）
5. 如果结果不确定，自动用 LLM 重新分析

## ⚙️ 增强的规则判断

规则判断已经大幅增强，现在包括：

### 扩展的关键词库

- **方法/技术**：method, approach, algorithm, technique, framework, model, architecture, system, deep learning, neural network, transformer, CNN, RNN, optimization, etc.
- **比较/评估**：compared, comparison, versus, outperforms, benchmark, evaluation, performance, accuracy, precision, recall, F1, improvement, etc.
- **事实性陈述**：shows, demonstrates, proves, indicates, suggests, reveals, finds, discovered, observed, confirms, validates, etc.
- **统计/数据**：statistical, significance, p-value, correlation, regression, analysis, dataset, sample, mean, variance, etc.
- **理论/概念**：theory, theoretical, theorem, proof, concept, principle, framework, hypothesis, assumption, definition, etc.
- **综述/相关工作**：survey, review, overview, state-of-the-art, related work, literature, previous, prior, existing, recent, etc.
- **基础性工作**：foundational, foundation, pioneering, seminal, original, first, introduced, proposed, established, classic, landmark, etc.
- **时间相关**：recent, recently, latest, new, novel, newly, current, contemporary, modern, state-of-the-art, 2020-2025, etc.

### 更专业的分类逻辑

- 10 种不同的意图类型
- 优先级判断（基础性工作 > 比较 > 方法 > 事实）
- 置信度评分
- 上下文感知

## 🐛 故障排除

### 问题 1：模式选择窗口不显示

**解决**：
- 确保已选中文本
- 检查是否有其他窗口遮挡
- 尝试移动鼠标到屏幕中央再按快捷键

### 问题 2：按 1/2/3 键没有反应

**解决**：
- 确保模式选择窗口有焦点
- 尝试点击窗口后再按数字键
- 检查键盘是否正常工作

### 问题 3：LLM 模式提示需要 API key

**解决**：
- 配置 API key（见上方配置说明）
- 或使用规则判断模式（模式 1）
- 或使用混合模式（模式 3），只在不确定时用 LLM

### 问题 4：混合模式总是用 LLM

**解决**：
- 混合模式只在结果不确定（Optional）时才用 LLM
- 如果规则判断结果是 Yes 或 No，不会调用 LLM
- 这是正常行为，可以节省 API 调用

## 💡 最佳实践

1. **日常使用**：默认选择规则判断（模式 1），快速免费
2. **重要论文**：选择 LLM 判断（模式 2），获得最高准确率
3. **平衡使用**：选择混合模式（模式 3），兼顾速度和准确率
4. **节省成本**：优先使用规则判断，只在必要时用 LLM

---

**现在就开始使用模式选择功能，获得最适合的分析体验！** 🚀
