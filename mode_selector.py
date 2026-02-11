"""
模式选择器 - 让用户选择分析模式
"""

from typing import Optional, Callable
import tkinter as tk
from enum import Enum


class AnalysisMode(Enum):
    """分析模式"""
    RULE_BASED = "rule"  # 规则判断
    LLM_BASED = "llm"    # LLM 判断
    HYBRID = "hybrid"    # 混合模式（先规则，不确定时用 LLM）


class ModeSelectorWindow:
    """模式选择窗口"""
    
    def __init__(self, callback: Callable[[AnalysisMode], None]):
        """
        Args:
            callback: 选择模式后的回调函数
        """
        self.callback = callback
        self.selected_mode: Optional[AnalysisMode] = None
        self.window: Optional[tk.Toplevel] = None
        self._root: Optional[tk.Tk] = None
    
    def _ensure_root(self):
        """确保根窗口存在"""
        if self._root is None:
            self._root = tk.Tk()
            self._root.withdraw()
    
    def show(self):
        """显示模式选择窗口"""
        self._ensure_root()
        
        if self.window:
            self.window.destroy()
        
        self.window = tk.Toplevel(self._root)
        self.window.title("选择分析模式")
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        
        # 设置窗口大小和位置
        width = 450
        height = 300
        try:
            x = self._root.winfo_pointerx() + 20
            y = self._root.winfo_pointery() + 20
        except:
            x = 100
            y = 100
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
        # 设置窗口背景
        self.window.configure(bg="#2b2b2b")
        
        # 标题
        title_label = tk.Label(
            self.window,
            text="选择分析模式",
            font=("Arial", 14, "bold"),
            bg="#2b2b2b",
            fg="#ffffff"
        )
        title_label.pack(pady=15)
        
        # 模式选项
        modes = [
            ("1", AnalysisMode.RULE_BASED, "规则判断（默认）", 
             "快速、免费、无需 API key\n准确率：70-80%"),
            ("2", AnalysisMode.LLM_BASED, "LLM 判断", 
             "更准确、需要 API key\n准确率：85-95%"),
            ("3", AnalysisMode.HYBRID, "混合模式", 
             "先规则判断，不确定时用 LLM\n平衡速度和准确率")
        ]
        
        self.mode_buttons = []
        for key, mode, title, desc in modes:
            frame = tk.Frame(self.window, bg="#2b2b2b")
            frame.pack(fill=tk.X, padx=20, pady=5)
            
            btn = tk.Button(
                frame,
                text=f"[{key}] {title}",
                command=lambda m=mode: self._select_mode(m),
                bg="#444444",
                fg="#ffffff",
                font=("Arial", 11),
                relief=tk.FLAT,
                padx=15,
                pady=10,
                anchor="w",
                width=40,
                cursor="hand2"
            )
            btn.pack(fill=tk.X)
            
            # 鼠标悬停效果
            def on_enter(e):
                btn.config(bg="#555555")
            def on_leave(e):
                btn.config(bg="#444444")
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            
            desc_label = tk.Label(
                frame,
                text=desc,
                font=("Arial", 9),
                bg="#2b2b2b",
                fg="#aaaaaa",
                justify=tk.LEFT
            )
            desc_label.pack(anchor="w", padx=15, pady=(0, 5))
            
            self.mode_buttons.append((key, mode, btn))
        
        # 绑定键盘事件
        self.window.bind('1', lambda e: self._select_mode(AnalysisMode.RULE_BASED))
        self.window.bind('2', lambda e: self._select_mode(AnalysisMode.LLM_BASED))
        self.window.bind('3', lambda e: self._select_mode(AnalysisMode.HYBRID))
        self.window.bind('<Escape>', lambda e: self._select_mode(None))
        
        # 设置焦点
        self.window.focus_force()
        self._root.update()
    
    def _select_mode(self, mode: Optional[AnalysisMode]):
        """选择模式"""
        self.selected_mode = mode
        if self.window:
            self.window.destroy()
            self.window = None
        
        if self.callback:
            self.callback(mode)
    
    def hide(self):
        """隐藏窗口"""
        if self.window:
            self.window.destroy()
            self.window = None


class ModeManager:
    """模式管理器"""
    
    def __init__(self, default_mode: AnalysisMode = AnalysisMode.RULE_BASED):
        """
        Args:
            default_mode: 默认模式
        """
        self.current_mode = default_mode
        self.llm_client = None
        self.selector = ModeSelectorWindow(self._on_mode_selected)
    
    def set_llm_client(self, llm_client):
        """设置 LLM 客户端"""
        self.llm_client = llm_client
    
    def _on_mode_selected(self, mode: Optional[AnalysisMode]):
        """模式选择回调"""
        if mode:
            self.current_mode = mode
            print(f"✅ 已选择模式: {mode.value}")
    
    def show_selector(self):
        """显示模式选择窗口"""
        self.selector.show()
    
    def get_agent(self):
        """根据当前模式获取 Agent"""
        from .agent import CitationAgent
        
        if self.current_mode == AnalysisMode.RULE_BASED:
            # 规则判断
            return CitationAgent(llm_client=None)
        elif self.current_mode == AnalysisMode.LLM_BASED:
            # LLM 判断
            if not self.llm_client:
                print("⚠️  LLM 模式需要配置 API key，回退到规则判断")
                return CitationAgent(llm_client=None)
            return CitationAgent(llm_client=self.llm_client)
        else:  # HYBRID
            # 混合模式：先规则，不确定时用 LLM
            return CitationAgent(llm_client=self.llm_client if self.llm_client else None)
    
    def analyze_with_mode(self, text: str) -> str:
        """使用当前模式分析文本"""
        agent = self.get_agent()
        result = agent.analyze(text)
        
        # 混合模式：如果结果不确定，且配置了 LLM，则用 LLM 再分析一次
        if (self.current_mode == AnalysisMode.HYBRID and 
            self.llm_client and 
            "Optional" in result):
            print("  🔄 混合模式：结果不确定，使用 LLM 重新分析...")
            llm_agent = CitationAgent(llm_client=self.llm_client)
            llm_result = llm_agent.analyze(text)
            return llm_result
        
        return result
