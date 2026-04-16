@echo off
chcp 65001 >nul
title VN Fear and Greed - Auto Watcher

echo Dang khoi dong Auto Watcher...
echo Cua so nay se chay nen. Dung tat cua so nay khi con muon tu dong push.
echo.

:: Kiem tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LOI] Python chua duoc cai dat!
    echo Vui long tai tai: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Chay watcher
python "%~dp0watcher.py"

pause
