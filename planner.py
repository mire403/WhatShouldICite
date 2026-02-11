"""
Citation Type Planner - 规划应该引用什么类型的工作
"""

from typing import List, Dict, Any, Optional
from .intent import CitationIntentClassifier


class CitationTypePlanner:
    """引用类型规划器"""
    
    def __init__(self, llm_client: Optional[Any] = None):
        """
        Args:
            llm_client: LLM 客户端（可选）
        """
        self.llm_client = llm_client
        self.intent_classifier = CitationIntentClassifier(llm_client)
    
    def plan(self, text: str) -> List[str]:
        """
        规划引用类型
        
        Args:
            text: 选中的文本
        
        Returns:
            引用类型建议列表
        """
        intent_result = self.intent_classifier.classify(text)
        intent = intent_result.get("intent", "unknown")
        
        # 如果提供了 LLM 客户端，使用 LLM 规划
        if self.llm_client:
            return self._plan_with_llm(text, intent)
        
        # 否则使用规则规划
        return self._plan_with_rules(text, intent)
    
    def _plan_with_rules(self, text: str, intent: str) -> List[str]:
        """基于规则的规划（增强版，更专业）"""
        text_lower = text.lower()
        suggestions = []
        
        if intent == "foundational_work":
            suggestions.append("The original/foundational paper introducing this concept")
            suggestions.append("Seminal works establishing the theoretical foundation")
        
        elif intent == "method_technique":
            # 根据具体技术领域给出建议
            if any(kw in text_lower for kw in ["deep learning", "neural network", "neural", "cnn", "rnn", "transformer"]):
                suggestions.append("Foundational works on deep learning and neural networks")
                suggestions.append("Recent advances in deep learning architectures")
                suggestions.append("State-of-the-art neural network methods")
            elif any(kw in text_lower for kw in ["optimization", "gradient", "adam", "sgd"]):
                suggestions.append("Foundational works on optimization algorithms")
                suggestions.append("Recent optimization methods and techniques")
            elif any(kw in text_lower for kw in ["reinforcement", "rl", "q-learning"]):
                suggestions.append("Foundational works on reinforcement learning")
                suggestions.append("Recent advances in RL algorithms")
            elif any(kw in text_lower for kw in ["computer vision", "image", "visual"]):
                suggestions.append("Foundational works on computer vision")
                suggestions.append("Recent computer vision methods")
            elif any(kw in text_lower for kw in ["nlp", "natural language", "language model"]):
                suggestions.append("Foundational works on natural language processing")
                suggestions.append("Recent NLP methods and language models")
            else:
                suggestions.append("Foundational works on the method/technique")
                suggestions.append("Recent advances in this technique")
                suggestions.append("State-of-the-art methods in this area")
        
        elif intent == "comparison":
            suggestions.append("Benchmark studies comparing different approaches")
            suggestions.append("Comparative evaluations of existing methods")
            suggestions.append("Performance analysis studies")
        
        elif intent == "factual_claim" or intent == "theoretical_claim":
            suggestions.append("Empirical studies demonstrating this claim")
            suggestions.append("Theoretical works supporting this statement")
            suggestions.append("Recent research validating this finding")
        
        elif intent == "survey_review":
            suggestions.append("Comprehensive surveys on this topic")
            suggestions.append("Recent review papers")
            suggestions.append("State-of-the-art overviews")
        
        elif intent == "recent_advance":
            suggestions.append("Recent advances in this area")
            suggestions.append("State-of-the-art methods")
            suggestions.append("Latest research developments")
        
        elif intent == "common_knowledge":
            return []  # 不需要引用
        
        else:
            suggestions.append("Related works on this topic")
            suggestions.append("Relevant research in this area")
        
        return suggestions
    
    def _plan_with_llm(self, text: str, intent: str) -> List[str]:
        """使用 LLM 规划"""
        from .llm_client import UnifiedLLMClient
        
        if not isinstance(self.llm_client, UnifiedLLMClient):
            unified_client = UnifiedLLMClient(self.llm_client)
        else:
            unified_client = self.llm_client
        
        return unified_client.plan_citation_types(text, intent)
