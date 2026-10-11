@echo off
REM Personal Financial Analyst - 部署腳本 (Windows)

echo ======================================
echo 個人財務分析師 - 自動部署
echo ======================================
echo.

REM 檢查 Git 是否已初始化
if not exist ".git" (
    echo 初始化 Git repository...
    git init
)

REM 添加所有文件
echo 添加文件到 Git...
git add .

REM 提交
set /p commit_message="請輸入提交訊息 (默認: Update code): "
if "%commit_message%"=="" set commit_message=Update code

git commit -m "%commit_message%"

REM 檢查是否已設置遠程 repository
git remote | findstr origin >nul 2>&1
if errorlevel 1 (
    echo.
    echo 請輸入您的 GitHub repository URL:
    echo 格式: https://github.com/YOUR_USERNAME/PersonalFinancialAnalyst.git
    set /p repo_url="URL: "
    
    if not "%repo_url%"=="" (
        git remote add origin "%repo_url%"
        echo ✓ 已添加遠程 repository
    ) else (
        echo ✗ 未提供 repository URL，跳過推送
        exit /b 1
    )
)

REM 推送到 GitHub
echo.
echo 推送到 GitHub...
git push -u origin main
if errorlevel 1 (
    git push -u origin master
)

echo.
echo ======================================
echo ✓ 部署完成！
echo ======================================
echo.
echo 下一步：
echo 1. 訪問您的 GitHub repository
echo 2. 查看 Actions 標籤，確認自動部署狀態
echo 3. 等待部署完成
echo.
echo 本地測試：
echo   python app.py
echo   訪問 http://localhost:5000
echo.
pause
