"""
测试模式选择功能
"""

from whatshouldicite.mode_selector import ModeManager, AnalysisMode
from whatshouldicite.agent import CitationAgent

def test_rules():
    """测试规则判断"""
    print("=" * 60)
    print("测试规则判断模式")
    print("=" * 60)
    
    test_cases = [
        "Deep learning has revolutionized computer vision in recent years.",
        "It is well known that water boils at 100 degrees Celsius.",
        "Our method outperforms previous approaches by 5% on the benchmark dataset.",
        "The transformer architecture was introduced in 2017.",
        "Recent studies have shown significant improvements in accuracy.",
    ]
    
    mode_manager = ModeManager(default_mode=AnalysisMode.RULE_BASED)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【测试用例 {i}】")
        print(f"文本: {text}")
        result = mode_manager.analyze_with_mode(text)
        print("结果:")
        print(result)
        print("-" * 60)

def test_mode_manager():
    """测试模式管理器"""
    print("=" * 60)
    print("测试模式管理器")
    print("=" * 60)
    
    mode_manager = ModeManager(default_mode=AnalysisMode.RULE_BASED)
    
    test_text = "Deep learning has revolutionized computer vision in recent years."
    
    print(f"\n测试文本: {test_text}")
    print("\n测试不同模式:")
    
    # 规则模式
    mode_manager.current_mode = AnalysisMode.RULE_BASED
    print("\n[1] 规则判断模式:")
    result1 = mode_manager.analyze_with_mode(test_text)
    print(result1[:200] + "...")
    
    # 如果有 LLM，测试 LLM 模式
    try:
        from whatshouldicite.llm_client import OpenAIClient, UnifiedLLMClient
        import os
        
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print("\n[2] LLM 判断模式:")
            client = OpenAIClient(api_key=api_key)
            unified_client = UnifiedLLMClient(client)
            mode_manager.set_llm_client(unified_client)
            mode_manager.current_mode = AnalysisMode.LLM_BASED
            result2 = mode_manager.analyze_with_mode(test_text)
            print(result2[:200] + "...")
        else:
            print("\n[2] LLM 判断模式: 未配置 API key，跳过")
    except Exception as e:
        print(f"\n[2] LLM 判断模式: 测试失败 - {e}")

if __name__ == "__main__":
    print("WhatShouldICite - 模式选择功能测试")
    print()
    
    # 测试规则判断
    test_rules()
    
    # 测试模式管理器
    # test_mode_manager()
    
    print("\n✅ 测试完成！")
