"""
Agent 命令行测试入口
实际使用时，编辑器会调用 whatshouldicite.CitationAgent
"""

from whatshouldicite import CitationAgent


def main():
    """
    命令行测试入口
    实际使用时，编辑器会调用 agent.analyze(selected_text)
    """
    agent = CitationAgent()
    
    # 测试用例
    test_cases = [
        "Deep learning has revolutionized computer vision in recent years.",
        "It is well known that water boils at 100 degrees Celsius.",
        "Our method outperforms previous approaches by 5% on the benchmark dataset.",
        "The transformer architecture was introduced in 2017.",
    ]
    
    print("=" * 60)
    print("WhatShouldICite Agent - 测试")
    print("=" * 60)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【测试用例 {i}】")
        print(f"选中文本: {text}")
        print("\n" + "-" * 60)
        result = agent.analyze(text)
        print(result)
        print("-" * 60)


if __name__ == "__main__":
    main()
