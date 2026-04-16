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

echo [1/4] Dang kiem tra thay doi...
git status --short

:: Kiem tra co thay doi khong
git diff --quiet %CSV_FILE% 2>nul
if %errorlevel% equ 0 (
    git ls-files --error-unmatch %CSV_FILE% >nul 2>&1
    if %errorlevel% equ 0 (
        echo [INFO] File CSV khong co thay doi moi. Bo qua push.
        timeout /t 3 >nul
        exit /b 0
    )
)

:: Lay ngay thang de ghi vao commit message
for /f "tokens=1-3 delims=/" %%a in ("%date%") do (
    set DD=%%a
    set MM=%%b
    set YYYY=%%c
)
set COMMIT_DATE=%YYYY%-%MM%-%DD%

echo [2/4] Dang stage file CSV...
git add %CSV_FILE%

echo [3/4] Dang commit...
git commit -m "update: market data %COMMIT_DATE%"

echo [4/4] Dang push len GitHub...
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
