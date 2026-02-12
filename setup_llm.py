"""
LLM 设置助手 - 帮助用户配置 LLM
"""

import os
import sys


def setup_openai():
    """设置 OpenAI"""
    try:
        from whatshouldicite.llm_client import OpenAIClient, UnifiedLLMClient
        
        api_key = input("请输入 OpenAI API Key: ").strip()
        if not api_key:
            print("❌ API Key 不能为空")
            return None
        
        model = input("请输入模型名称 (默认: gpt-3.5-turbo): ").strip() or "gpt-3.5-turbo"
        
        client = OpenAIClient(api_key=api_key, model=model)
        unified_client = UnifiedLLMClient(client)
        
        print("✅ OpenAI 配置成功！")
        return unified_client
        
    except ImportError:
        print("❌ OpenAI SDK 未安装。请运行: pip install openai")
        return None
    except Exception as e:
        print(f"❌ 配置失败: {e}")
        return None


def setup_anthropic():
    """设置 Anthropic"""
    try:
        from whatshouldicite.llm_client import AnthropicClient, UnifiedLLMClient
        
        api_key = input("请输入 Anthropic API Key: ").strip()
        if not api_key:
            print("❌ API Key 不能为空")
            return None
        
        model = input("请输入模型名称 (默认: claude-3-haiku-20240307): ").strip() or "claude-3-haiku-20240307"
        
        client = AnthropicClient(api_key=api_key, model=model)
        unified_client = UnifiedLLMClient(client)
        
        print("✅ Anthropic 配置成功！")
        return unified_client
        
    except ImportError:
        print("❌ Anthropic SDK 未安装。请运行: pip install anthropic")
        return None
    except Exception as e:
        print(f"❌ 配置失败: {e}")
        return None


def main():
    """主函数"""
    print("=" * 60)
    print("WhatShouldICite - LLM 配置助手")
    print("=" * 60)
    print()
    print("请选择要使用的 LLM：")
    print("1. OpenAI (GPT-3.5/GPT-4)")
    print("2. Anthropic (Claude)")
    print("3. 不使用 LLM（仅规则判断）")
    print()
    
    choice = input("请输入选项 (1/2/3): ").strip()
    
    if choice == "1":
        llm_client = setup_openai()
        if llm_client:
            print("\n✅ 配置完成！")
            print("\n使用方法：")
            print("```python")
            print("from whatshouldicite import CitationAgent")
            print("from whatshouldicite.llm_client import OpenAIClient, UnifiedLLMClient")
            print()
            print("client = OpenAIClient(api_key='your-key', model='gpt-3.5-turbo')")
            print("unified_client = UnifiedLLMClient(client)")
            print("agent = CitationAgent(llm_client=unified_client)")
            print("```")
    elif choice == "2":
        llm_client = setup_anthropic()
        if llm_client:
            print("\n✅ 配置完成！")
            print("\n使用方法：")
            print("```python")
            print("from whatshouldicite import CitationAgent")
            print("from whatshouldicite.llm_client import AnthropicClient, UnifiedLLMClient")
            print()
            print("client = AnthropicClient(api_key='your-key')")
            print("unified_client = UnifiedLLMClient(client)")
            print("agent = CitationAgent(llm_client=unified_client)")
            print("```")
    elif choice == "3":
        print("\n✅ 将使用规则判断（默认模式）")
        print("无需任何配置，直接使用即可！")
    else:
        print("❌ 无效选项")


if __name__ == "__main__":
    main()
