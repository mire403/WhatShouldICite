"""
系统级浮窗显示模块
"""

import tkinter as tk
from tkinter import scrolledtext
from typing import Optional
import threading


class CitationPopupWindow:
    """引用建议浮窗"""
    
    def __init__(self):
        self.window: Optional[tk.Tk] = None
        self.text_widget: Optional[scrolledtext.ScrolledText] = None
    
    def show(self, content: str, x: Optional[int] = None, y: Optional[int] = None):
        """
        显示浮窗
        
        Args:
            content: 要显示的内容
            x, y: 窗口位置（None 则显示在鼠标位置附近）
        """
        # 如果窗口已存在，先关闭
        if self.window:
            self.hide()
        
        # 创建新窗口
        self.window = tk.Tk()
        self.window.title("WhatShouldICite")
        
        # 设置窗口属性
        self.window.overrideredirect(True)  # 无边框
        self.window.attributes('-topmost', True)  # 置顶
        self.window.attributes('-alpha', 0.95)  # 半透明（可选）
        
        # 设置窗口大小
        width = 500
        height = 400
        self.window.geometry(f"{width}x{height}")
        
        # 设置窗口位置
        if x is None or y is None:
            # 获取鼠标位置
            x = self.window.winfo_pointerx()
            y = self.window.winfo_pointery()
            # 稍微偏移，避免遮挡鼠标
            x += 20
            y += 20
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
        # 创建文本显示区域
        self.text_widget = scrolledtext.ScrolledText(
            self.window,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#2b2b2b",  # 深色背景
            fg="#ffffff",  # 白色文字
            insertbackground="#ffffff",
            borderwidth=0,
            padx=15,
            pady=15
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # 插入内容
        self.text_widget.insert("1.0", content)
        self.text_widget.config(state=tk.DISABLED)  # 只读
        
        # 添加关闭按钮
        close_btn = tk.Button(
            self.window,
            text="关闭 (Esc)",
            command=self.hide,
            bg="#444444",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        close_btn.pack(pady=5)
        
        # 绑定 ESC 键关闭
        self.window.bind('<Escape>', lambda e: self.hide())
        self.window.bind('<Button-1>', lambda e: self._on_click_outside(e))
        
        # 设置焦点
        self.window.focus_force()
        
        # 显示窗口（非阻塞）
        self.window.after(100, self._show_window)
    
    def _show_window(self):
        """显示窗口（在主线程中）"""
        if self.window:
            try:
                self.window.mainloop()
            except:
                pass
    
    def show_async(self, content: str, x: Optional[int] = None, y: Optional[int] = None):
        """异步显示浮窗（在新线程中）"""
        thread = threading.Thread(
            target=self.show,
            args=(content, x, y),
            daemon=True
        )
        thread.start()
    
    def _on_click_outside(self, event):
        """点击窗口外部时关闭"""
        # 简单实现：点击窗口本身不关闭
        # 可以改进：检测点击是否在窗口外
        pass
    
    def hide(self):
        """隐藏浮窗"""
        if self.window:
            try:
                self.window.quit()
                self.window.destroy()
            except:
                pass
            self.window = None
            self.text_widget = None


class SimplePopupWindow:
    """简化版浮窗（使用更轻量的实现）"""
    
    def __init__(self):
        self.window: Optional[tk.Toplevel] = None
        self._root: Optional[tk.Tk] = None
    
    def _ensure_root(self):
        """确保根窗口存在"""
        if self._root is None:
            self._root = tk.Tk()
            self._root.withdraw()  # 隐藏根窗口
    
    def show(self, content: str):
        """显示浮窗"""
        # 如果已有窗口，先关闭
        if self.window:
            self.hide()
        
        # 确保根窗口存在
        self._ensure_root()
        
        # 创建浮窗
        self.window = tk.Toplevel(self._root)
        self.window.title("WhatShouldICite")
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        
        width = 500
        height = 400
        try:
            x = self._root.winfo_pointerx() + 20
            y = self._root.winfo_pointery() + 20
        except:
            x = 100
            y = 100
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
        # 文本显示
        text_widget = scrolledtext.ScrolledText(
            self.window,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#2b2b2b",
            fg="#ffffff",
            borderwidth=0,
            padx=15,
            pady=15
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert("1.0", content)
        text_widget.config(state=tk.DISABLED)
        
        # 关闭按钮
        close_btn = tk.Button(
            self.window,
            text="关闭 (Esc)",
            command=self.hide,
            bg="#444444",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        close_btn.pack(pady=5)
        
        self.window.bind('<Escape>', lambda e: self.hide())
        self.window.focus_force()
        
        # 更新窗口（非阻塞）
        self._root.update()
    
    def hide(self):
        """隐藏浮窗"""
        if self.window:
            try:
                self.window.destroy()
            except:
                pass
            self.window = None
