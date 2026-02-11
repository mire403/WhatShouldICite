"""
Text Analyzer - 分析选中文本的基本特征
"""

from typing import Dict, Any
from .utils import clean_text


class TextAnalyzer:
    """文本分析器 - 提取文本特征"""
    
    def __init__(self):
        pass
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        分析文本特征
        
        Args:
            text: 选中的文本
        
        Returns:
            包含文本特征的字典
        """
        cleaned = clean_text(text)
        
        # 基本统计
        word_count = len(cleaned.split())
        sentence_count = cleaned.count('.') + cleaned.count('!') + cleaned.count('?')
        
        # 检测关键词模式（扩展的学术关键词库）
        text_lower = cleaned.lower()
        
        # 方法/技术关键词（扩展）
        method_keywords = [
            'method', 'approach', 'algorithm', 'technique', 'framework',
            'model', 'architecture', 'system', 'mechanism', 'strategy',
            'procedure', 'protocol', 'scheme', 'design', 'implementation',
            'deep learning', 'neural network', 'transformer', 'cnn', 'rnn',
            'optimization', 'gradient', 'backpropagation', 'training',
            'inference', 'prediction', 'classification', 'regression'
        ]
        has_method_keywords = any(kw in text_lower for kw in method_keywords)
        
        # 比较/评估关键词（扩展）
        comparison_keywords = [
            'compared', 'comparison', 'compare', 'versus', 'vs', 'v.s.',
            'better', 'worse', 'superior', 'inferior', 'outperforms',
            'outperformed', 'exceeds', 'surpasses', 'beats', 'than',
            'benchmark', 'evaluation', 'evaluate', 'performance',
            'accuracy', 'precision', 'recall', 'f1', 'f-score',
            'improvement', 'improved', 'enhancement', 'enhanced'
        ]
        has_comparison_keywords = any(kw in text_lower for kw in comparison_keywords)
        
        # 事实性陈述关键词（扩展）
        factual_keywords = [
            'shows', 'show', 'demonstrates', 'demonstrate', 'proves', 'prove',
            'indicates', 'indicate', 'suggests', 'suggest', 'reveals', 'reveal',
            'finds', 'find', 'found', 'discovered', 'discover',
            'observed', 'observe', 'exhibits', 'exhibit', 'presents', 'present',
            'confirms', 'confirm', 'validates', 'validate', 'verifies', 'verify',
            'establishes', 'establish', 'evidence', 'empirical', 'experiment',
            'study', 'studies', 'research', 'paper', 'work', 'works'
        ]
        has_factual_keywords = any(kw in text_lower for kw in factual_keywords)
        
        # 统计/数据关键词
        statistical_keywords = [
            'statistical', 'statistics', 'significant', 'significance',
            'p-value', 'p value', 'correlation', 'regression', 'analysis',
            'dataset', 'data', 'sample', 'population', 'mean', 'median',
            'variance', 'standard deviation', 'confidence interval'
        ]
        has_statistical_keywords = any(kw in text_lower for kw in statistical_keywords)
        
        # 理论/概念关键词
        theoretical_keywords = [
            'theory', 'theoretical', 'theorem', 'proof', 'prove',
            'concept', 'conceptual', 'principle', 'framework', 'paradigm',
            'hypothesis', 'hypotheses', 'assumption', 'assumptions',
            'definition', 'formal', 'mathematical', 'mathematically'
        ]
        has_theoretical_keywords = any(kw in text_lower for kw in theoretical_keywords)
        
        # 综述/相关工作关键词
        survey_keywords = [
            'survey', 'review', 'overview', 'state-of-the-art', 'sota',
            'related work', 'related works', 'literature', 'previous',
            'prior', 'existing', 'recent', 'recently', 'latest'
        ]
        has_survey_keywords = any(kw in text_lower for kw in survey_keywords)
        
        # 基础性工作关键词
        foundational_keywords = [
            'foundational', 'foundation', 'pioneering', 'seminal',
            'original', 'first', 'introduced', 'proposed', 'propose',
            'established', 'establish', 'classic', 'landmark'
        ]
        has_foundational_keywords = any(kw in text_lower for kw in foundational_keywords)
        
        # 时间相关关键词（最新进展）
        temporal_keywords = [
            'recent', 'recently', 'latest', 'new', 'novel', 'newly',
            'current', 'contemporary', 'modern', 'state-of-the-art',
            '2020', '2021', '2022', '2023', '2024', '2025'
        ]
        has_temporal_keywords = any(kw in text_lower for kw in temporal_keywords)
        
        return {
            "text": cleaned,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "has_method_keywords": has_method_keywords,
            "has_comparison_keywords": has_comparison_keywords,
            "has_factual_keywords": has_factual_keywords,
            "has_statistical_keywords": has_statistical_keywords,
            "has_theoretical_keywords": has_theoretical_keywords,
            "has_survey_keywords": has_survey_keywords,
            "has_foundational_keywords": has_foundational_keywords,
            "has_temporal_keywords": has_temporal_keywords,
            "is_short": word_count < 20,
            "is_long": word_count > 100
        }
