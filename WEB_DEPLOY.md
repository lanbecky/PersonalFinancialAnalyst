# 網頁版部署指南

## 📦 項目概述

個人財務分析師現在提供完整的網頁版本！包含：
- 🎨 現代化響應式網頁界面
- 🚀 Flask REST API 後端
- 🐳 Docker 容器化部署
- ⚙️ GitHub Actions 自動部署

## 🌐 網頁版本架構

```
網頁應用
├── 前端 (HTML/CSS/JavaScript)
│   ├── templates/index.html
│   ├── static/css/style.css
│   └── static/js/app.js
│
├── 後端 (Flask API)
│   ├── app.py
│   └── 原有 Python 模組
│
└── 部署配置
    ├── Dockerfile
    ├── docker-compose.yml
    └── .github/workflows/
```

## 🚀 快速開始

### 方法 1: 本地運行

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 啟動 Flask 應用
python app.py

# 3. 瀏覽器打開
http://localhost:5000
```

### 方法 2: Docker 運行

```bash
# 1. 構建 Docker 映像
docker build -t financial-analyst .

# 2. 運行容器
docker run -p 5000:5000 financial-analyst

# 3. 瀏覽器打開
http://localhost:5000
```

### 方法 3: Docker Compose

```bash
# 一鍵啟動
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down
```

## 📤 GitHub 部署步驟

### 1. 創建 GitHub Repository

```bash
# 初始化 Git (如果尚未初始化)
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Personal Financial Analyst Web App"

# 連接到 GitHub (替換成您的 repository URL)
git remote add origin https://github.com/YOUR_USERNAME/PersonalFinancialAnalyst.git

# 推送到 GitHub
git push -u origin main
```

### 2. 配置 GitHub Actions

GitHub Actions 會自動觸發在：
- ✅ 推送到 main 分支時
- ✅ 創建 Pull Request 時
- ✅ 手動觸發時

workflows 包括：
1. **deploy.yml** - 構建和測試
2. **docker-publish.yml** - Docker 映像發佈

### 3. 啟用 GitHub Pages (可選)

如果您想部署靜態前端到 GitHub Pages：

1. 進入 Repository Settings
2. 找到 "Pages" 部分
3. Source 選擇 "GitHub Actions"
4. Actions 會自動部署 `static` 目錄

## 🌍 部署到雲端平台

### Heroku 部署

```bash
# 1. 登入 Heroku
heroku login

# 2. 創建應用
heroku create your-app-name

# 3. 推送部署
git push heroku main

# 4. 打開應用
heroku open
```

需要創建 `Procfile`:
```
web: gunicorn app:app
```

### Railway 部署

1. 訪問 [railway.app](https://railway.app)
2. 連接 GitHub repository
3. 選擇項目
4. Railway 會自動檢測 Dockerfile 並部署

### Render 部署

1. 訪問 [render.com](https://render.com)
2. 創建 New Web Service
3. 連接 GitHub repository
4. 配置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

### Google Cloud Run

```bash
# 1. 構建並推送映像
gcloud builds submit --tag gcr.io/PROJECT_ID/financial-analyst

# 2. 部署到 Cloud Run
gcloud run deploy financial-analyst \
  --image gcr.io/PROJECT_ID/financial-analyst \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🔧 環境變量配置

創建 `.env` 文件 (本地開發):
```bash
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here
```

生產環境變量:
```bash
FLASK_ENV=production
FLASK_DEBUG=0
GUNICORN_WORKERS=4
```

## 📊 API 端點

### 分析查詢
```
POST /api/analyze
Content-Type: application/json

{
  "query": "Compare AAPL and MSFT revenue"
}
```

### 獲取範例
```
GET /api/examples
```

### 查詢歷史
```
GET /api/history
```

### 系統狀態
```
GET /api/status
```

### 可用工具
```
GET /api/tools
```

### 健康檢查
```
GET /health
```

## 🎨 前端功能

### 主要功能
- ✅ 即時財務分析
- ✅ 執行步驟可視化
- ✅ 結果格式化顯示
- ✅ 查詢歷史記錄
- ✅ 範例查詢快速選擇
- ✅ 響應式設計 (手機/平板/桌面)

### 使用方式
1. 輸入您的財務查詢
2. 點擊「開始分析」
3. 查看執行過程
4. 閱讀分析結果

## 🐳 Docker 詳細配置

### Dockerfile 說明
- 基於 Python 3.11
- 多階段構建 (可選優化)
- Gunicorn 生產服務器
- 健康檢查配置

### Docker Compose 說明
- 單服務配置
- 自動重啟
- 端口映射
- 健康檢查

## 🔒 安全考慮

### 生產環境
1. **使用 HTTPS**
   - 配置 SSL/TLS 證書
   - 使用反向代理 (Nginx/Caddy)

2. **環境變量**
   - 不要在代碼中硬編碼密鑰
   - 使用環境變量或密鑰管理服務

3. **速率限制**
   - 添加 API 速率限制
   - 防止濫用

4. **CORS 配置**
   - 根據需要限制來源
   - 不要在生產中使用 `*`

### 示例 Nginx 配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📈 監控和日誌

### 查看應用日誌
```bash
# Docker
docker logs financial-analyst

# Docker Compose
docker-compose logs -f web
```

### 健康檢查
```bash
curl http://localhost:5000/health
```

### 系統狀態
```bash
curl http://localhost:5000/api/status
```

## 🐛 故障排除

### 問題 1: 端口已被占用
```bash
# 更改端口
docker run -p 8080:5000 financial-analyst
```

### 問題 2: 依賴安裝失敗
```bash
# 清理並重新安裝
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### 問題 3: Docker 構建失敗
```bash
# 清理 Docker 緩存
docker system prune -a
docker build --no-cache -t financial-analyst .
```

### 問題 4: API 響應緩慢
- 增加 Gunicorn workers 數量
- 優化查詢複雜度
- 添加緩存層 (Redis)

## 📝 自定義配置

### 修改端口
在 `app.py` 中:
```python
app.run(host='0.0.0.0', port=8080)
```

### 修改樣式
編輯 `static/css/style.css`

### 修改功能
編輯 `static/js/app.js`

### 添加新 API 端點
在 `app.py` 中添加新路由:
```python
@app.route('/api/your-endpoint')
def your_endpoint():
    return jsonify({'data': 'value'})
```

## 🎯 後續增強

可以考慮添加:
- [ ] 用戶認證系統
- [ ] 數據庫持久化 (PostgreSQL/MongoDB)
- [ ] Redis 緩存層
- [ ] WebSocket 實時更新
- [ ] 圖表可視化 (Chart.js/D3.js)
- [ ] PDF 報告生成
- [ ] API 密鑰管理
- [ ] 多語言支持

## 💡 使用提示

1. **開發模式**: 使用 `python app.py` 方便調試
2. **生產模式**: 使用 Docker 或 Gunicorn
3. **測試**: 運行 `python test_system.py` 確保功能正常
4. **部署**: 選擇適合的雲平台 (Heroku, Railway, Render)

## 📞 技術支持

遇到問題？
1. 檢查日誌輸出
2. 查看 GitHub Issues
3. 閱讀相關文檔

---

**🎉 恭喜！您的網頁版財務分析師已準備就緒！**

訪問 `http://localhost:5000` 開始使用。
