@echo off
REM WhatShouldICite 全局服务启动脚本
REM Windows 批处理文件

echo ============================================================
echo WhatShouldICite - 全局 Agent 服务
echo ============================================================
echo.
echo 提示：Windows 上需要管理员权限才能注册全局快捷键
echo 如果启动失败，请右键此文件，选择"以管理员身份运行"
echo.
echo 按任意键继续...
pause >nul

python run_global_agent.py

pause
