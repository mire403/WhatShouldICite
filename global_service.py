"""
全局服务模块 - 实现跨应用的全局快捷键和浮窗
"""

import threading
import time
from typing import Optional, Callable
import sys

try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


class GlobalHotkeyService:
    """全局快捷键服务"""
    
    def __init__(self, hotkey: str = "ctrl+shift+c", callback: Optional[Callable] = None):
        """
        Args:
            hotkey: 快捷键组合，如 "ctrl+shift+c"
            callback: 快捷键触发时的回调函数
        """
        self.hotkey = hotkey
        self.callback = callback
        self.running = False
        self.hotkey_thread = None
    
    def start(self):
        """启动全局快捷键监听"""
        if not KEYBOARD_AVAILABLE:
            raise ImportError(
                "keyboard 模块未安装。请运行: pip install keyboard\n"
                "注意：Windows 上需要管理员权限才能注册全局快捷键"
            )
        
        if self.running:
            return
        
        self.running = True
        
        def on_hotkey():
            try:
                keyboard.add_hotkey(self.hotkey, self._on_triggered)
                keyboard.wait()  # 阻塞直到程序退出
            except Exception as e:
                print(f"快捷键注册失败: {e}")
                print("提示：Windows 上可能需要管理员权限")
        
        self.hotkey_thread = threading.Thread(target=on_hotkey, daemon=True)
        self.hotkey_thread.start()
        print(f"✅ 全局快捷键已注册: {self.hotkey}")
        print("   按 Ctrl+C 退出程序")
    
    def _on_triggered(self):
        """快捷键触发时的处理"""
        if self.callback:
            try:
                self.callback()
            except Exception as e:
                print(f"回调函数执行失败: {e}")
    
    def stop(self):
        """停止全局快捷键监听"""
        self.running = False
        if KEYBOARD_AVAILABLE:
            try:
                keyboard.unhook_all()
            except:
                pass


class ClipboardTextGetter:
    """通过剪贴板获取选中文本"""
    
    def __init__(self):
        if not CLIPBOARD_AVAILABLE:
            raise ImportError(
                "pyperclip 模块未安装。请运行: pip install pyperclip"
            )
    
    def get_selected_text(self) -> Optional[str]:
        """
        获取当前选中的文本
        
        方法：模拟 Ctrl+C，然后从剪贴板读取
        注意：这会覆盖剪贴板内容
        
        Returns:
            选中的文本，如果没有选中则返回 None
        """
        try:
            # 保存当前剪贴板内容
            old_clipboard = pyperclip.paste()
            
            # 模拟 Ctrl+C
            try:
                import pyautogui
                pyautogui.hotkey('ctrl', 'c')
            except ImportError:
                raise ImportError("pyautogui 模块未安装。请运行: pip install pyautogui")
            
            # 等待剪贴板更新
            time.sleep(0.1)
            
            # 读取剪贴板
            selected_text = pyperclip.paste()
            
            # 如果内容没变，说明没有选中文本
            if selected_text == old_clipboard:
                return None
            
            # 恢复剪贴板（可选）
            # pyperclip.copy(old_clipboard)
            
            return selected_text.strip() if selected_text else None
            
        except Exception as e:
            print(f"获取选中文本失败: {e}")
            return None


def get_selected_text_windows() -> Optional[str]:
    """
    Windows 专用：使用 Windows API 获取选中文本（不依赖剪贴板）
    
    需要 pywin32
    """
    try:
        import win32clipboard
        import win32con
        
        # 保存当前剪贴板
        win32clipboard.OpenClipboard()
        try:
            old_data = win32clipboard.GetClipboardData()
        except:
            old_data = None
        win32clipboard.CloseClipboard()
        
        # 模拟 Ctrl+C
        try:
            import pyautogui
            pyautogui.hotkey('ctrl', 'c')
        except ImportError:
            # 如果没有 pyautogui，使用 pyperclip 方法
            getter = ClipboardTextGetter()
            return getter.get_selected_text()
        
        time.sleep(0.1)
        
        # 读取剪贴板
        win32clipboard.OpenClipboard()
        try:
            text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        except:
            text = None
        win32clipboard.CloseClipboard()
        
        if text and text != old_data:
            return text.strip()
        return None
        
    except ImportError:
        # 如果没有 pywin32，使用 pyperclip
        getter = ClipboardTextGetter()
        return getter.get_selected_text()
    except Exception as e:
        print(f"获取选中文本失败: {e}")
        return None
