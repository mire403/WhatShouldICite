"""
使用 LLM 启动全局 Agent 服务
"""

import sys
import os

# 尝试从环境变量或配置文件读取 API key
def get_llm_client():
    """获取 LLM 客户端"""
    # 优先使用环境变量
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    # 如果环境变量没有，尝试读取配置文件
    if not openai_key and not anthropic_key:
        try:
            import config
            openai_key = getattr(config, "OPENAI_API_KEY", None)
            anthropic_key = getattr(config, "ANTHROPIC_API_KEY", None)
            use_llm = getattr(config, "USE_LLM", "none")
        except ImportError:
            print("⚠️  未找到 config.py 配置文件")
            print("   将使用规则判断模式（无需 API key）")
            return None
    
    # 选择 LLM
    if openai_key and openai_key != "your-openai-api-key-here":
        try:
            from whatshouldicite.llm_client import OpenAIClient, UnifiedLLMClient
            print("✅ 使用 OpenAI")
            client = OpenAIClient(api_key=openai_key)
            return UnifiedLLMClient(client)
        except Exception as e:
            print(f"⚠️  OpenAI 初始化失败: {e}")
            print("   将使用规则判断模式")
            return None
    
    elif anthropic_key and anthropic_key != "your-anthropic-api-key-here":
        try:
            from whatshouldicite.llm_client import AnthropicClient, UnifiedLLMClient
            print("✅ 使用 Anthropic Claude")
            client = AnthropicClient(api_key=anthropic_key)
            return UnifiedLLMClient(client)
        except Exception as e:
            print(f"⚠️  Anthropic 初始化失败: {e}")
            print("   将使用规则判断模式")
            return None
    
    else:
        print("ℹ️  未配置 LLM API key，使用规则判断模式")
        return None


def main():
    """主函数"""
    print("=" * 60)
    print("WhatShouldICite - 全局 Agent 服务（LLM 模式）")
    print("=" * 60)
    print()
    
    # 获取 LLM 客户端
    llm_client = get_llm_client()
    
    if llm_client:
        print("✅ LLM 模式已启用")
    else:
        print("ℹ️  使用规则判断模式（无需 API key）")
    
    print()
    
    # 启动全局服务
    from whatshouldicite.global_agent import GlobalCitationAgent
    from whatshouldicite.mode_selector import AnalysisMode
    
    try:
        # 如果配置了 LLM，默认使用混合模式；否则使用规则模式
        default_mode = AnalysisMode.HYBRID if llm_client else AnalysisMode.RULE_BASED
        agent = GlobalCitationAgent(llm_client=llm_client, default_mode=default_mode)
        agent.start()
    except KeyboardInterrupt:
        print("\n\n程序已退出")
    except Exception as e:
        print(f"\n\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
