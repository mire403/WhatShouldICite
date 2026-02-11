"""
Keyword Generator - 生成检索关键词
"""

from typing import List, Dict, Any, Optional
import re
from .analyzer import TextAnalyzer
from .planner import CitationTypePlanner


class KeywordGenerator:
    """关键词生成器"""
    
    def __init__(self, llm_client: Optional[Any] = None):
        """
        Args:
            llm_client: LLM 客户端（可选）
        """
        self.llm_client = llm_client
        self.analyzer = TextAnalyzer()
        self.planner = CitationTypePlanner(llm_client)
    
    def generate(self, text: str, citation_types: List[str]) -> List[str]:
        """
        生成检索关键词
        
        Args:
            text: 选中的文本
            citation_types: 引用类型列表
        
        Returns:
            关键词列表
        """
        # 如果提供了 LLM 客户端，使用 LLM 生成
        if self.llm_client:
            return self._generate_with_llm(text, citation_types)
        
        # 否则使用规则生成
        return self._generate_with_rules(text, citation_types)
    
    def _generate_with_rules(self, text: str, citation_types: List[str]) -> List[str]:
        """基于规则的关键词生成"""
        analysis = self.analyzer.analyze(text)
        keywords = []
        
        # 提取名词短语（简单规则）
        words = text.lower().split()
        
        # 移除停用词
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
            'could', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
        
        # 提取重要名词（长度 > 3，非停用词）
        important_words = [
            w.strip('.,!?;:()[]{}"\'') 
            for w in words 
            if len(w) > 3 and w not in stop_words
        ]
        
        # 生成关键词组合
        if important_words:
            # 单个关键词
            keywords.extend(important_words[:3])
            
            # 双词组合
            if len(important_words) >= 2:
                keywords.append(f"{important_words[0]} {important_words[1]}")
            if len(important_words) >= 3:
                keywords.append(f"{important_words[1]} {important_words[2]}")
        
        # 基于引用类型添加领域特定关键词
        for ct in citation_types:
            ct_lower = ct.lower()
            if "deep learning" in ct_lower or "neural" in ct_lower:
                keywords.extend(["deep learning", "neural networks", "neural network methods"])
            elif "optimization" in ct_lower:
                keywords.extend(["optimization algorithms", "optimization methods"])
            elif "benchmark" in ct_lower or "comparison" in ct_lower:
                keywords.extend(["benchmark evaluation", "performance comparison"])
            elif "computer vision" in ct_lower or "vision" in ct_lower:
                keywords.extend(["computer vision", "image processing"])
            elif "nlp" in ct_lower or "natural language" in ct_lower:
                keywords.extend(["natural language processing", "nlp methods"])
            elif "reinforcement" in ct_lower:
                keywords.extend(["reinforcement learning", "rl algorithms"])
        
        # 基于文本内容提取领域关键词
        text_lower = text.lower()
        domain_keywords_map = {
            "machine learning": ["machine learning", "ml methods"],
            "artificial intelligence": ["artificial intelligence", "ai methods"],
            "data mining": ["data mining", "data analysis"],
            "statistics": ["statistical methods", "statistical analysis"],
            "optimization": ["optimization", "optimization algorithms"],
            "graph": ["graph algorithms", "graph theory"],
            "network": ["network analysis", "network methods"]
        }
        
        for domain, kws in domain_keywords_map.items():
            if domain in text_lower:
                keywords.extend(kws)
                break
        
        # 去重并限制数量
        keywords = list(dict.fromkeys(keywords))[:5]
        
        return keywords
    
    def _generate_with_llm(self, text: str, citation_types: List[str]) -> List[str]:
        """使用 LLM 生成"""
        from .llm_client import UnifiedLLMClient
        
        if not isinstance(self.llm_client, UnifiedLLMClient):
            unified_client = UnifiedLLMClient(self.llm_client)
        else:
            unified_client = self.llm_client
        
        return unified_client.generate_keywords(text, citation_types)
