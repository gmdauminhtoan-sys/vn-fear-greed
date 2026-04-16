@echo off
chcp 65001 >nul
echo ============================================
echo   SETUP GIT - VN Fear and Greed Index
echo ============================================
echo.

:: Kiem tra Git da cai chua
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LOI] Git chua duoc cai dat!
    echo Vui long tai Git tai: https://git-scm.com/download/win
    pause
    exit /b 1
)

:: Chuyen vao thu muc lam viec
cd /d E:\APP\vn-fear-greed

:: Kiem tra da la git repo chua
if exist ".git" (
    echo [INFO] Thu muc nay da la git repository.
    git remote set-url origin https://github.com/gmdauminhtoan-sys/vn-fear-greed.git
    echo [OK] Da cap nhat remote URL.
) else (
    echo [INFO] Khoi tao git repository...
    git init
    git remote add origin https://github.com/gmdauminhtoan-sys/vn-fear-greed.git
    git fetch origin
    git checkout -b main --track origin/main
    echo [OK] Da ket noi voi GitHub.
)

:: Cau hinh thong tin user
git config user.name "Minh Toan"
git config user.email "gmdauminhtoan@gmail.com"

:: Luu token vao Git Credential Manager (Windows Credential Store)
echo.
echo [BUOC CUOI] Luu thong tin xac thuc GitHub...
echo Nhap GitHub Personal Access Token cua ban:
set /p TOKEN="> "

git credential approve << EOF
protocol=https
host=github.com
username=gmdauminhtoan-sys
password=%TOKEN%
EOF

:: Thu push de kiem tra
echo.
echo [KIEM TRA] Thu ket noi voi GitHub...
git ls-remote origin >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo   SETUP THANH CONG!
    echo   Ban co the dung push_to_github.bat
    echo   hoac start_watcher.bat tu bay gio.
    echo ============================================
) else (
    echo [LOI] Khong the ket noi. Kiem tra lai token.
)

echo.
pause
