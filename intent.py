"""
Citation Intent Classifier - 分类引用意图
"""

from typing import Dict, Any, Optional
from .analyzer import TextAnalyzer


class CitationIntentClassifier:
    """引用意图分类器"""
    
    def __init__(self, llm_client: Optional[Any] = None):
        """
        Args:
            llm_client: LLM 客户端（可选，如果为 None 则使用规则判断）
        """
        self.llm_client = llm_client
        self.analyzer = TextAnalyzer()
    
    def classify(self, text: str) -> Dict[str, Any]:
        """
        分类引用意图
        
        Args:
            text: 选中的文本
        
        Returns:
            包含分类结果的字典
        """
        analysis = self.analyzer.analyze(text)
        
        # 如果提供了 LLM 客户端，使用 LLM 分类
        if self.llm_client:
            return self._classify_with_llm(text)
        
        # 否则使用规则判断
        return self._classify_with_rules(analysis)
    
    def _classify_with_rules(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """基于规则的分类（增强版，更专业更学术）"""
        text = analysis["text"].lower()
        
        # 1. 常识判断（不需要引用）- 扩展模式
        common_knowledge_patterns = [
            "it is well known", "it is well-known", "well known that",
            "as we all know", "as everyone knows", "as is known",
            "obviously", "clearly", "it is clear that", "it is clear",
            "it is obvious", "it is evident", "evidently",
            "common sense", "common knowledge", "widely known",
            "universally accepted", "generally accepted",
            "water boils at", "the sun rises", "gravity", "earth is round"
        ]
        
        if any(pattern in text for pattern in common_knowledge_patterns):
            return {
                "intent": "common_knowledge",
                "needs_citation": "No",
                "confidence": 0.85
            }
        
        # 2. 基础性工作（高优先级）
        if analysis["has_foundational_keywords"]:
            return {
                "intent": "foundational_work",
                "needs_citation": "Yes",
                "confidence": 0.9
            }
        
        # 3. 综述/相关工作
        if analysis["has_survey_keywords"]:
            return {
                "intent": "survey_review",
                "needs_citation": "Yes",
                "confidence": 0.85
            }
        
        # 4. 比较/评估（高优先级）
        if analysis["has_comparison_keywords"]:
            return {
                "intent": "comparison",
                "needs_citation": "Yes",
                "confidence": 0.9
            }
        
        # 5. 方法/技术（高优先级）
        if analysis["has_method_keywords"]:
            # 结合时间关键词判断是否为最新进展
            if analysis["has_temporal_keywords"]:
                return {
                    "intent": "recent_advance",
                    "needs_citation": "Yes",
                    "confidence": 0.85
                }
            return {
                "intent": "method_technique",
                "needs_citation": "Yes",
                "confidence": 0.85
            }
        
        # 6. 理论/概念
        if analysis["has_theoretical_keywords"]:
            return {
                "intent": "theoretical_claim",
                "needs_citation": "Yes",
                "confidence": 0.8
            }
        
        # 7. 统计/数据（事实性陈述）
        if analysis["has_statistical_keywords"]:
            return {
                "intent": "factual_claim",
                "needs_citation": "Yes",
                "confidence": 0.85
            }
        
        # 8. 事实性陈述
        if analysis["has_factual_keywords"]:
            return {
                "intent": "factual_claim",
                "needs_citation": "Yes",
                "confidence": 0.8
            }
        
        # 9. 最新进展（时间相关）
        if analysis["has_temporal_keywords"]:
            return {
                "intent": "recent_advance",
                "needs_citation": "Yes",
                "confidence": 0.75
            }
        
        # 10. 默认：可选（需要人工判断）
        return {
            "intent": "unknown",
            "needs_citation": "Optional",
            "confidence": 0.5
        }
    
    def _classify_with_llm(self, text: str) -> Dict[str, Any]:
        """使用 LLM 分类"""
        from .llm_client import UnifiedLLMClient
        
        if not isinstance(self.llm_client, UnifiedLLMClient):
            # 如果不是 UnifiedLLMClient，尝试包装
            unified_client = UnifiedLLMClient(self.llm_client)
        else:
            unified_client = self.llm_client
        
        return unified_client.classify_intent(text)
