"""
Agent 入口 - 处理编辑器传入的选中文本，返回引用建议
"""

from typing import Optional, Dict, Any
from .intent import CitationIntentClassifier
from .planner import CitationTypePlanner
from .keywords import KeywordGenerator
from .utils import format_output, clean_text


class CitationAgent:
    """
    引用建议 Agent
    
    核心职责：
    - 接收编辑器传入的 selection text
    - 调用核心分析逻辑
    - 返回适合浮窗显示的结果
    """
    
    def __init__(self, llm_client: Optional[Any] = None):
        """
        Args:
            llm_client: LLM 客户端（可选，如果为 None 则使用规则判断）
        """
        self.intent_classifier = CitationIntentClassifier(llm_client)
        self.planner = CitationTypePlanner(llm_client)
        self.keyword_generator = KeywordGenerator(llm_client)
    
    def analyze(self, selected_text: str) -> str:
        """
        分析选中文本，返回格式化建议
        
        Args:
            selected_text: 用户选中的文本（1-5 句话）
        
        Returns:
            格式化后的引用建议字符串，适合在浮窗中显示
        """
        if not selected_text or not selected_text.strip():
            return self._empty_result()
        
        # 清理文本
        text = clean_text(selected_text)
        
        # 如果使用 LLM，尝试一次性分析
        if self.intent_classifier.llm_client:
            try:
                from .llm_client import UnifiedLLMClient
                
                # 获取统一的 LLM 客户端
                if isinstance(self.intent_classifier.llm_client, UnifiedLLMClient):
                    unified_client = self.intent_classifier.llm_client
                else:
                    # 如果不是 UnifiedLLMClient，尝试包装
                    unified_client = UnifiedLLMClient(self.intent_classifier.llm_client)
                
                # 使用 LLM 完整分析
                result = unified_client.analyze_citation(text)
                
                # 如果 LLM 分析成功，直接使用结果
                if "error" not in result:
                    return format_output(
                        needs_citation=result.get("needs_citation", "Optional"),
                        reason=result.get("reason", "需要进一步分析"),
                        citation_types=result.get("citation_types", []),
                        keywords=result.get("keywords", [])
                    )
            except Exception as e:
                # LLM 分析失败，回退到规则判断
                import sys
                print(f"⚠️  LLM 分析失败，使用规则判断: {e}", file=sys.stderr)
        
        # 使用规则判断或 LLM 分步分析
        # 1. 分类引用意图
        intent_result = self.intent_classifier.classify(text)
        needs_citation = intent_result.get("needs_citation", "Optional")
        intent = intent_result.get("intent", "unknown")
        
        # 2. 生成原因说明
        reason = self._generate_reason(intent, needs_citation)
        
        # 3. 规划引用类型
        citation_types = []
        if needs_citation != "No":
            citation_types = self.planner.plan(text)
        
        # 4. 生成关键词
        keywords = []
        if needs_citation != "No":
            keywords = self.keyword_generator.generate(text, citation_types)
        
        # 5. 格式化输出
        return format_output(
            needs_citation=needs_citation,
            reason=reason,
            citation_types=citation_types,
            keywords=keywords
        )
    
    def _generate_reason(self, intent: str, needs_citation: str) -> str:
        """生成原因说明"""
        reason_map = {
            "common_knowledge": "这是常识性陈述，通常不需要引用",
            "method_technique": "提到了具体方法或技术，需要引用相关研究",
            "comparison": "进行了比较或评估，需要引用被比较的工作",
            "factual_claim": "这是事实性陈述，需要引用支持性研究",
            "survey_review": "提到了综述性工作，建议引用相关综述",
            "foundational_work": "提到了基础性工作，建议引用原始文献",
            "recent_advance": "提到了最新进展，需要引用相关研究",
            "unknown": "建议检查是否需要引用相关研究"
        }
        
        if needs_citation == "No":
            return reason_map.get(intent, "不需要引用")
        elif needs_citation == "Optional":
            return reason_map.get(intent, "可能需要引用，取决于上下文")
        else:
            return reason_map.get(intent, "需要引用相关研究")
    
    def _empty_result(self) -> str:
        """返回空结果"""
        return format_output(
            needs_citation="No",
            reason="未选中文本",
            citation_types=[],
            keywords=[]
        )
