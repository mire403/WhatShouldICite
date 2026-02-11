"""
工具函数
"""

import re
from typing import Optional


def clean_text(text: str) -> str:
    """清理选中文本，移除多余空白"""
    if not text:
        return ""
    # 移除首尾空白，合并多个空白字符
    text = re.sub(r'\s+', ' ', text.strip())
    return text


def format_output(
    needs_citation: str,
    reason: str,
    citation_types: list[str],
    keywords: list[str]
) -> str:
    """
    格式化输出为适合浮窗显示的格式
    
    Args:
        needs_citation: "Yes" / "Optional" / "No"
        reason: 简短原因说明
        citation_types: 引用类型列表
        keywords: 关键词列表
    
    Returns:
        格式化后的字符串
    """
    # 确定图标
    icon_map = {
        "Yes": "✔️",
        "Optional": "⚠️",
        "No": "❌"
    }
    icon = icon_map.get(needs_citation, "❓")
    
    output = []
    output.append("【Do I need a citation?】")
    output.append(f"{icon} {needs_citation}")
    output.append("")
    output.append("【Why】")
    output.append(f"- {reason}")
    output.append("")
    
    if needs_citation != "No" and citation_types:
        output.append("【What to cite】")
        for ct in citation_types:
            output.append(f"- {ct}")
        output.append("")
    
    if keywords:
        output.append("【Search keywords】")
        for kw in keywords:
            output.append(f'- "{kw}"')
    
    return "\n".join(output)


def parse_llm_response(response: str) -> dict:
    """
    解析 LLM 响应（如果使用结构化输出）
    这里提供一个基础解析函数，实际使用时可能需要根据 LLM 输出格式调整
    """
    # 这是一个占位实现，实际应该根据使用的 LLM API 返回格式来解析
    return {
        "needs_citation": "Yes",
        "reason": "需要引用相关研究",
        "citation_types": [],
        "keywords": []
    }
