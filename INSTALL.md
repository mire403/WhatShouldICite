# 安装和使用指南

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装项目

```bash
pip install -e .
```

## Windows 使用说明

### ⚠️ 重要提示

**Windows 上运行全局服务需要管理员权限！**

全局快捷键功能需要管理员权限才能注册系统级快捷键。

### 启动全局服务

1. **以管理员身份运行 PowerShell 或 CMD**

2. 运行：
```bash
python run_global_agent.py
```

3. 看到以下提示说明启动成功：
```
============================================================
WhatShouldICite - 全局 Agent 服务
============================================================
快捷键: ctrl+shift+c
使用说明：
  1. 在任何应用中选中文本
  2. 按下快捷键触发分析
  3. 查看浮窗中的引用建议
  4. 按 ESC 关闭浮窗
============================================================
```

### 使用方法

1. **在任何应用中选中文本**（编辑器、浏览器、Word、WPS 等）
2. **按下 `Ctrl + Shift + C`**
3. **查看浮窗**中的引用建议
4. **按 `ESC` 关闭浮窗**

### 自定义快捷键

```bash
python run_global_agent.py --hotkey "ctrl+alt+c"
```

支持的快捷键格式：
- `ctrl+shift+c`
- `ctrl+alt+c`
- `win+shift+c`
- 等等

## 故障排除

### 问题 1：快捷键无法注册

**症状**：启动时提示需要管理员权限

**解决**：
- 以管理员身份运行 PowerShell/CMD
- 右键点击 PowerShell/CMD，选择"以管理员身份运行"

### 问题 2：无法获取选中文本

**症状**：按快捷键后提示"未检测到选中的文本"

**解决**：
1. 确保已选中文本（文本高亮显示）
2. 某些应用可能不支持 Ctrl+C 复制选中文本
3. 尝试手动复制（Ctrl+C）后再按快捷键

### 问题 3：浮窗不显示

**症状**：分析完成但看不到浮窗

**解决**：
1. 检查是否有其他窗口遮挡
2. 浮窗可能显示在屏幕外，尝试移动鼠标到屏幕中央再触发
3. 检查 Python 是否安装了 tkinter（通常随 Python 安装）

### 问题 4：依赖安装失败

**症状**：`pip install` 报错

**解决**：
1. 更新 pip：`python -m pip install --upgrade pip`
2. 某些包可能需要编译工具（Windows 上通常有预编译版本）
3. 如果 `keyboard` 安装失败，可以尝试：`pip install keyboard --no-cache-dir`

## 开发模式

如果修改了代码，无需重新安装，直接运行即可。

## 后台运行（可选）

### Windows 任务计划程序

可以将程序设置为开机自启动：

1. 打开"任务计划程序"
2. 创建基本任务
3. 触发器：用户登录时
4. 操作：启动程序 `pythonw.exe`，参数：`run_global_agent.py` 的完整路径

### 使用 NSSM（推荐）

NSSM 可以将 Python 脚本注册为 Windows 服务：

```bash
# 下载 NSSM
# 安装服务
nssm install WhatShouldICite "C:\Python\python.exe" "C:\path\to\run_global_agent.py"
nssm start WhatShouldICite
```

## 卸载

```bash
pip uninstall whatshouldicite
```
