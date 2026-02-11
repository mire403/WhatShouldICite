"""
LLM 客户端抽象层 - 支持多种大模型
"""

from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import json
import re


class LLMClient(ABC):
    """LLM 客户端抽象基类"""
    
    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> str:
        """完成文本生成"""
        pass


class OpenAIClient(LLMClient):
    """OpenAI API 客户端"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Args:
            api_key: OpenAI API key
            model: 模型名称，默认 gpt-3.5-turbo
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI SDK 未安装。请运行: pip install openai"
            )
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def complete(self, prompt: str, **kwargs) -> str:
        """调用 OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get("temperature", 0.3),
                max_tokens=kwargs.get("max_tokens", 500)
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenAI API 调用失败: {e}")


class AnthropicClient(LLMClient):
    """Anthropic Claude API 客户端"""
    
    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307"):
        """
        Args:
            api_key: Anthropic API key
            model: 模型名称，默认 claude-3-haiku-20240307
        """
        try:
            import anthropic
        except ImportError:
            raise ImportError(
                "Anthropic SDK 未安装。请运行: pip install anthropic"
            )
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    def complete(self, prompt: str, **kwargs) -> str:
        """调用 Anthropic API"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", 500),
                temperature=kwargs.get("temperature", 0.3),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            raise Exception(f"Anthropic API 调用失败: {e}")


class UnifiedLLMClient:
    """统一的 LLM 客户端接口"""
    
    def __init__(self, client: LLMClient):
        """
        Args:
            client: LLM 客户端实例（OpenAIClient 或 AnthropicClient）
        """
        self.client = client
    
    def analyze_citation(self, text: str) -> Dict[str, Any]:
        """
        使用 LLM 分析引用需求
        
        Returns:
            包含分析结果的字典
        """
        from .prompts import ANALYZE_PROMPT
        
        prompt = ANALYZE_PROMPT.format(selected_text=text)
        
        try:
            response = self.client.complete(prompt)
            return self._parse_analysis_response(response, text)
        except Exception as e:
            # 如果 LLM 调用失败，返回错误信息
            return {
                "needs_citation": "Optional",
                "reason": f"LLM 分析失败: {str(e)}",
                "citation_types": [],
                "keywords": [],
                "intent": "unknown",
                "error": str(e)
            }
    
    def classify_intent(self, text: str) -> Dict[str, Any]:
        """使用 LLM 分类引用意图"""
        from .prompts import INTENT_CLASSIFY_PROMPT
        
        prompt = INTENT_CLASSIFY_PROMPT.format(text=text)
        
        try:
            response = self.client.complete(prompt, max_tokens=50)
            intent = self._parse_intent(response)
            
            # 根据意图判断是否需要引用
            needs_citation = self._intent_to_citation_need(intent)
            
            return {
                "intent": intent,
                "needs_citation": needs_citation,
                "confidence": 0.9  # LLM 判断置信度较高
            }
        except Exception as e:
            return {
                "intent": "unknown",
                "needs_citation": "Optional",
                "confidence": 0.5,
                "error": str(e)
            }
    
    def plan_citation_types(self, text: str, intent: str) -> List[str]:
        """使用 LLM 规划引用类型"""
        from .prompts import PLANNER_PROMPT
        
        prompt = PLANNER_PROMPT.format(text=text, intent=intent)
        
        try:
            response = self.client.complete(prompt, max_tokens=200)
            return self._parse_citation_types(response)
        except Exception as e:
            return []
    
    def generate_keywords(self, text: str, citation_types: List[str]) -> List[str]:
        """使用 LLM 生成关键词"""
        from .prompts import KEYWORD_PROMPT
        
        citation_type_str = "\n".join(citation_types) if citation_types else "General research"
        prompt = KEYWORD_PROMPT.format(text=text, citation_type=citation_type_str)
        
        try:
            response = self.client.complete(prompt, max_tokens=150)
            return self._parse_keywords(response)
        except Exception as e:
            return []
    
    def _parse_analysis_response(self, response: str, text: str) -> Dict[str, Any]:
        """解析完整的分析响应"""
        # 尝试提取结构化信息
        needs_citation = self._extract_citation_need(response)
        reason = self._extract_reason(response)
        citation_types = self._extract_citation_types(response)
        keywords = self._extract_keywords(response)
        intent = self._infer_intent_from_response(response)
        
        return {
            "needs_citation": needs_citation,
            "reason": reason,
            "citation_types": citation_types,
            "keywords": keywords,
            "intent": intent
        }
    
    def _extract_citation_need(self, response: str) -> str:
        """提取是否需要引用"""
        response_lower = response.lower()
        if "yes" in response_lower and "no" not in response_lower[:50]:
            return "Yes"
        elif "no" in response_lower and "yes" not in response_lower[:50]:
            return "No"
        elif "optional" in response_lower:
            return "Optional"
        return "Optional"
    
    def _extract_reason(self, response: str) -> str:
        """提取原因说明"""
        # 查找 "why" 或 "原因" 后面的内容
        patterns = [
            r"(?:why|原因)[：:]\s*(.+?)(?:\n|$)",
            r"因为(.+?)(?:\n|$)",
            r"(.+?)(?:需要引用|不需要引用)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                reason = match.group(1).strip()
                if len(reason) > 100:
                    reason = reason[:100] + "..."
                return reason
        
        # 如果没有找到，返回第一句话
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) > 10:
                return line[:100]
        
        return "需要进一步分析"
    
    def _extract_citation_types(self, response: str) -> List[str]:
        """提取引用类型"""
        types = []
        
        # 查找 "what to cite" 或 "引用" 部分
        patterns = [
            r"(?:what to cite|引用类型|应该引用)[：:]\s*(.+?)(?:\n\n|\Z)",
            r"[-•]\s*(Foundational works|Recent methods|Surveys)(.+?)(?:\n|$)"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if isinstance(match, tuple):
                    match = " ".join(match)
                match = match.strip()
                if match and len(match) > 10:
                    types.append(match)
        
        # 如果没有找到，尝试提取所有以 "-" 开头的行
        if not types:
            for line in response.split('\n'):
                line = line.strip()
                if line.startswith('-') or line.startswith('•'):
                    line = line.lstrip('-•').strip()
                    if "foundational" in line.lower() or "recent" in line.lower() or "survey" in line.lower():
                        types.append(line)
        
        return types[:5]  # 最多返回 5 个
    
    def _extract_keywords(self, response: str) -> List[str]:
        """提取关键词"""
        keywords = []
        
        # 查找引号中的关键词
        quoted = re.findall(r'"([^"]+)"', response)
        keywords.extend(quoted)
        
        # 查找 "keywords" 部分的行
        in_keywords_section = False
        for line in response.split('\n'):
            if "keyword" in line.lower():
                in_keywords_section = True
                continue
            if in_keywords_section:
                line = line.strip()
                if line.startswith('-') or line.startswith('•'):
                    kw = line.lstrip('-•').strip().strip('"')
                    if kw:
                        keywords.append(kw)
                elif line and '"' not in line:
                    keywords.append(line.strip())
        
        return keywords[:5]  # 最多返回 5 个
    
    def _parse_intent(self, response: str) -> str:
        """解析意图类型"""
        response_lower = response.lower().strip()
        
        intent_map = {
            "factual": "factual_claim",
            "method": "method_technique",
            "technique": "method_technique",
            "comparison": "comparison",
            "survey": "survey_review",
            "review": "survey_review",
            "foundational": "foundational_work",
            "recent": "recent_advance",
            "common": "common_knowledge",
            "knowledge": "common_knowledge"
        }
        
        for key, intent in intent_map.items():
            if key in response_lower:
                return intent
        
        return "unknown"
    
    def _intent_to_citation_need(self, intent: str) -> str:
        """将意图转换为引用需求"""
        if intent == "common_knowledge":
            return "No"
        elif intent in ["method_technique", "comparison", "factual_claim", "survey_review", "foundational_work", "recent_advance"]:
            return "Yes"
        else:
            return "Optional"
    
    def _parse_citation_types(self, response: str) -> List[str]:
        """解析引用类型列表"""
        types = []
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('-') or line.startswith('•'):
                line = line.lstrip('-•').strip()
                if line and len(line) > 10:
                    types.append(line)
        return types[:5]
    
    def _parse_keywords(self, response: str) -> List[str]:
        """解析关键词列表"""
        keywords = []
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('-') or line.startswith('•'):
                line = line.lstrip('-•').strip().strip('"')
                if line:
                    keywords.append(line)
            elif line and '"' in line:
                # 提取引号中的内容
                quoted = re.findall(r'"([^"]+)"', line)
                keywords.extend(quoted)
        return keywords[:5]
    
    def _infer_intent_from_response(self, response: str) -> str:
        """从响应中推断意图"""
        response_lower = response.lower()
        
        if "method" in response_lower or "technique" in response_lower:
            return "method_technique"
        elif "comparison" in response_lower or "compare" in response_lower:
            return "comparison"
        elif "survey" in response_lower or "review" in response_lower:
            return "survey_review"
        elif "foundational" in response_lower:
            return "foundational_work"
        elif "recent" in response_lower:
            return "recent_advance"
        elif "common" in response_lower or "well known" in response_lower:
            return "common_knowledge"
        else:
            return "factual_claim"
