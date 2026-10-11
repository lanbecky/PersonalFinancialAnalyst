#!/bin/bash

# Personal Financial Analyst - 部署腳本

echo "======================================"
echo "個人財務分析師 - 自動部署"
echo "======================================"
echo ""

# 檢查 Git 是否已初始化
if [ ! -d ".git" ]; then
    echo "初始化 Git repository..."
    git init
fi

# 添加所有文件
echo "添加文件到 Git..."
git add .

# 提交
echo "請輸入提交訊息 (默認: Update code):"
read commit_message
if [ -z "$commit_message" ]; then
    commit_message="Update code"
fi

git commit -m "$commit_message"

# 檢查是否已設置遠程 repository
if ! git remote | grep -q origin; then
    echo ""
    echo "請輸入您的 GitHub repository URL:"
    echo "格式: https://github.com/YOUR_USERNAME/PersonalFinancialAnalyst.git"
    read repo_url
    
    if [ ! -z "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✓ 已添加遠程 repository"
    else
        echo "✗ 未提供 repository URL，跳過推送"
        exit 1
    fi
fi

# 推送到 GitHub
echo ""
echo "推送到 GitHub..."
git push -u origin main || git push -u origin master

echo ""
echo "======================================"
echo "✓ 部署完成！"
echo "======================================"
echo ""
echo "下一步："
echo "1. 訪問您的 GitHub repository"
echo "2. 查看 Actions 標籤，確認自動部署狀態"
echo "3. 等待部署完成"
echo ""
echo "本地測試："
echo "  python app.py"
echo "  訪問 http://localhost:5000"
echo ""
