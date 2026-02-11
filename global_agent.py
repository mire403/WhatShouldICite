"""
全局 Agent 服务 - 整合全局快捷键、文本获取和浮窗显示
"""

import sys
from typing import Optional
from .agent import CitationAgent
from .global_service import GlobalHotkeyService, get_selected_text_windows
from .popup_window import SimplePopupWindow
from .mode_selector import ModeManager, AnalysisMode


class GlobalCitationAgent:
    """全局引用建议 Agent"""
    
    def __init__(self, hotkey: str = "ctrl+shift+c", llm_client=None, default_mode: AnalysisMode = AnalysisMode.RULE_BASED):
        """
        Args:
            hotkey: 全局快捷键，默认 "ctrl+shift+c"
            llm_client: LLM 客户端（可选）
            default_mode: 默认分析模式
        """
        self.mode_manager = ModeManager(default_mode=default_mode)
        if llm_client:
            self.mode_manager.set_llm_client(llm_client)
        
        self.hotkey_service = GlobalHotkeyService(hotkey, self._on_hotkey_triggered)
        self.popup = SimplePopupWindow()
        self.running = False
        self.pending_text: Optional[str] = None  # 待分析的文本
    
    def start(self):
        """启动全局服务"""
        print("=" * 60)
        print("WhatShouldICite - 全局 Agent 服务")
        print("=" * 60)
        print(f"快捷键: {self.hotkey_service.hotkey}")
        print("使用说明：")
        print("  1. 在任何应用中选中文本")
        print("  2. 按下快捷键触发分析")
        print("  3. 选择分析模式（按 1/2/3 键）")
        print("     [1] 规则判断（默认，快速免费）")
        print("     [2] LLM 判断（更准确，需要 API key）")
        print("     [3] 混合模式（先规则，不确定时用 LLM）")
        print("  4. 查看浮窗中的引用建议")
        print("  5. 按 ESC 关闭浮窗")
        print("=" * 60)
        print()
        
        self.running = True
        self.hotkey_service.start()
        
        # 保持程序运行
        try:
            import keyboard
            keyboard.wait()  # 等待直到程序退出
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print(f"运行错误: {e}")
            self.stop()
    
    def _on_hotkey_triggered(self):
        """快捷键触发时的处理"""
        print("\n[快捷键触发] 正在获取选中文本...")
        
        # 获取选中文本
        selected_text = get_selected_text_windows()
        
        if not selected_text:
            print("  ⚠️ 未检测到选中的文本")
            self.popup.show("⚠️ 未检测到选中的文本\n\n请先选中一段文本，然后按快捷键。")
            return
        
        print(f"  选中文本: {selected_text[:50]}...")
        
        # 保存待分析的文本
        self.pending_text = selected_text
        
        # 显示模式选择窗口
        print("  显示模式选择窗口...")
        self.mode_manager.selector.callback = self._on_mode_selected
        self.mode_manager.show_selector()
    
    def _on_mode_selected(self, mode: Optional[AnalysisMode]):
        """模式选择后的处理"""
        if not self.pending_text:
            return
        
        if mode is None:
            print("  ❌ 已取消")
            return
        
        selected_text = self.pending_text
        self.pending_text = None
        
        print(f"  已选择模式: {mode.value}")
        print("  正在分析...")
        
        # 根据选择的模式分析文本
        try:
            result = self.mode_manager.analyze_with_mode(selected_text)
            print("  ✅ 分析完成，显示浮窗")
            
            # 显示结果浮窗
            self.popup.show(result)
            
        except Exception as e:
            error_msg = f"❌ 分析失败\n\n错误信息：{str(e)}"
            print(f"  {error_msg}")
            self.popup.show(error_msg)
    
    def stop(self):
        """停止服务"""
        print("\n正在停止服务...")
        self.running = False
        self.hotkey_service.stop()
        self.popup.hide()
        print("服务已停止")


def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="WhatShouldICite 全局 Agent 服务")
    parser.add_argument(
        "--hotkey",
        default="ctrl+shift+c",
        help="全局快捷键（默认: ctrl+shift+c）"
    )
    
    args = parser.parse_args()
    
    try:
        agent = GlobalCitationAgent(hotkey=args.hotkey)
        agent.start()
    except KeyboardInterrupt:
        print("\n\n程序已退出")
    except Exception as e:
        print(f"\n\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
