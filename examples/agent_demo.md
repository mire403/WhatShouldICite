# WhatShouldICite Agent 使用示例

## 示例 1：需要引用的方法描述

**选中文本：**
```
Deep learning has revolutionized computer vision in recent years.
```

**Agent 输出：**
```
【Do I need a citation?】
✔️ Yes

【Why】
- 提到了具体方法或技术，需要引用相关研究

【What to cite】
- Foundational works on deep learning
- Recent methods for neural networks

【Search keywords】
- "deep learning"
- "computer vision"
- "neural networks"
- "deep learning computer"
```

## 示例 2：常识性陈述（不需要引用）

**选中文本：**
```
It is well known that water boils at 100 degrees Celsius.
```

**Agent 输出：**
```
【Do I need a citation?】
❌ No

【Why】
- 这是常识性陈述，通常不需要引用
```

## 示例 3：比较性陈述

**选中文本：**
```
Our method outperforms previous approaches by 5% on the benchmark dataset.
```

**Agent 输出：**
```
【Do I need a citation?】
✔️ Yes

【Why】
- 进行了比较或评估，需要引用被比较的工作

【What to cite】
- Benchmark studies comparing different approaches
- Recent comparative evaluations

【Search keywords】
- "benchmark evaluation"
- "previous approaches"
- "method outperforms"
```

## 示例 4：事实性陈述

**选中文本：**
```
The transformer architecture was introduced in 2017.
```

**Agent 输出：**
```
【Do I need a citation?】
✔️ Yes

【Why】
- 这是事实性陈述，需要引用支持性研究

【What to cite】
- Foundational works on the method
- Recent advances in the technique

【Search keywords】
- "transformer architecture"
- "introduced 2017"
- "transformer architecture introduced"
```

## 使用场景

### 场景 1：写作中途检查

你在写论文，突然不确定某句话是否需要引用：

1. 选中这句话
2. 按 `Cmd + Shift + C`
3. 看到建议："需要引用相关研究"
4. 继续写作，稍后查找引用

### 场景 2：寻找引用方向

你知道需要引用，但不确定找什么：

1. 选中文本
2. 查看 "What to cite" 建议
3. 使用 "Search keywords" 在学术数据库中搜索

### 场景 3：确认常识

不确定某个陈述是否属于常识：

1. 选中文本
2. 看到 "❌ No" 和原因说明
3. 确认无需引用，继续写作

## 注意事项

- Agent **不会**给出具体的论文标题或作者名
- Agent **只**提供引用类型和检索关键词
- 最终决定是否需要引用，由作者自己判断
- Agent 的建议仅供参考，不保证完全准确
