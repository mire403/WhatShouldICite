"""
LLM 配置示例文件
复制此文件为 config.py 并填入你的 API key
"""

# ============================================
# OpenAI 配置
# ============================================
# 获取 API key: https://platform.openai.com/api-keys
OPENAI_API_KEY = "your-openai-api-key-here"
OPENAI_MODEL = "gpt-3.5-turbo"  # 或 "gpt-4", "gpt-4-turbo-preview"

# ============================================
# Anthropic Claude 配置
# ============================================
# 获取 API key: https://console.anthropic.com/
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"
ANTHROPIC_MODEL = "claude-3-haiku-20240307"  # 或 "claude-3-sonnet-20240229", "claude-3-opus-20240229"

# ============================================
# 使用哪个 LLM（可选值：openai, anthropic, none）
# ============================================
USE_LLM = "none"  # 改为 "openai" 或 "anthropic" 以启用 LLM
