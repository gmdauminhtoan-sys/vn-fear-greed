@echo off
chcp 65001 >nul

:: ============================================
::   PUSH CSV LEN GITHUB - VN Fear and Greed
::   Double-click sau khi export tu Amibroker
:: ============================================

set REPO_DIR=E:\APP\vn-fear-greed
set CSV_FILE=csv\update.csv

cd /d %REPO_DIR%

:: Kiem tra file CSV ton tai khong
if not exist "%CSV_FILE%" (
    echo [LOI] Khong tim thay file %CSV_FILE% trong %REPO_DIR%
    echo Vui long kiem tra lai Amibroker da export dung thu muc chua.
    pause
    exit /b 1
)

echo [1/6] Dang kiem tra thay doi...
git status --short

:: Kiem tra co thay doi khong
git diff --quiet %CSV_FILE% 2>nul
set HAS_CHANGES=%errorlevel%

if %HAS_CHANGES% equ 0 (
    echo [INFO] File CSV khong co thay doi moi. Chi dong bo voi remote.
    git pull --rebase origin main
    timeout /t 3 >nul
    exit /b 0
)

:: Lay ngay thang de ghi vao commit message
for /f "tokens=1-3 delims=/" %%a in ("%date%") do (
    set DD=%%a
    set MM=%%b
    set YYYY=%%c
)
set COMMIT_DATE=%YYYY%-%MM%-%DD%

echo [2/6] Dang stash thay doi CSV tam thoi...
git stash push -- %CSV_FILE%
if %errorlevel% neq 0 (
    echo [LOI] Stash that bai. Dung lai.
    pause
    exit /b 1
)

echo [3/6] Dang pull ban moi nhat tu GitHub (rebase)...
git pull --rebase origin main
if %errorlevel% neq 0 (
    echo [LOI] Pull that bai. Dang khoi phuc stash...
    git stash pop
    echo Vui long xu ly conflict thu cong roi chay lai.
    pause
    exit /b 1
)

echo [4/6] Dang khoi phuc thay doi CSV...
git stash pop
if %errorlevel% neq 0 (
    echo [LOI] Conflict khi pop stash. Xu ly thu cong.
    pause
    exit /b 1
)

echo [5/6] Dang commit...
git add %CSV_FILE%
git commit -m "update: market data %COMMIT_DATE%"

echo [6/6] Dang push len GitHub...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo   PUSH THANH CONG!
    echo   GitHub Actions se tu dong chay build.py
    echo   va cap nhat dashboard.
    echo ============================================
) else (
    echo.
    echo [LOI] Push that bai. Kiem tra ket noi mang
    echo hoac chay lai setup_git.bat neu token het han.
)

echo.
timeout /t 5 >nul
