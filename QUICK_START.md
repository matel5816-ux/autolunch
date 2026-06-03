# 🚀 AutoLunch 快速開始指南

完成整個專案從零到上線，預計 **4-6 小時**。

---

## 📋 檢查清單

### 第 0 步：蒐集必要信息（15 分鐘）

- [x] **公司位置**（已確認並驗證 ✅）
  - [x] 公司名稱：**群健科技 (Cofit)**
  - [x] 公司地址：**104臺北市中山區行政里松江路363號4樓**
  - [x] 座標（已驗證正確）：
    - 緯度：**25.0638409**
    - 經度：**121.5334954**
  - [x] ✅ **座標已驗證**：[Google Maps 官方位置](https://www.google.com/maps/place/Cofit+群健科技)

- [ ] **距離篩選選項**（已設定四個）
  - [x] 300m（步行4分鐘）
  - [x] 600m（步行7-8分鐘）
  - [x] 1km（步行13-15分鐘）
  - [x] 1.5km（步行18-20分鐘）
  - [ ] 決定是否需要「自訂距離」功能

- [ ] **LINE 官方帳戶**
  - [ ] LINE Developers 帳戶已開通
  - [ ] 新建一個 Provider
  - [ ] 新建一個 Messaging API Channel

- [ ] **Google API 金鑰**
  - [ ] Google Cloud Console 專案已建立
  - [ ] 啟用 Places API 和 Maps API
  - [ ] API 金鑰已複製

- [ ] **雲端平台帳戶**
  - [ ] Render 帳戶（推薦免費）或 Zeabur
  - [ ] GitHub 帳戶（用於連結 git repo）

---

## 🎯 分步驟執行

### **第 1 步：環境設定（30 分鐘）**

#### 1.1 複製專案
```bash
# 選項 A：從 GitHub 複製（若已上傳）
git clone https://github.com/your-username/autolunch.git
cd AutoLunch

# 選項 B：手動創建本地資料夾
mkdir AutoLunch
cd AutoLunch
git init
```

#### 1.2 建立 Python 虛擬環境
```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 1.3 安裝依賴
```bash
pip install -r requirements.txt
```

#### 1.4 設定環境變數
```bash
# 複製範本
cp .env.example .env

# 編輯 .env 檔案（使用編輯器打開）
# Windows: notepad .env
# macOS/Linux: nano .env

# 填入以下必要欄位：
# - LINE_CHANNEL_SECRET
# - LINE_CHANNEL_ACCESS_TOKEN
# - GOOGLE_MAPS_API_KEY
# - COMPANY_LATITUDE
# - COMPANY_LONGITUDE
```

✅ **檢查點**：執行 `python --version` 確認 Python 3.9+

---

### **第 2 步：資料庫初始化（1-2 小時）**

#### 2.1 建立項目目錄結構

```bash
# 自動建立所有必要目錄
python scripts/setup_project.py

# 或手動建立
mkdir -p src/models src/services src/handlers src/database src/utils
mkdir -p data tests logs scripts
```

#### 2.2 初始化 SQLite 資料庫

**方案 A：快速測試（推薦）**

```bash
# 填入示範餐廳資料
python scripts/populate_sample_data.py

# 驗證資料
python -c "
from src.database.queries import list_all_restaurants
restaurants = list_all_restaurants()
print(f'✅ 資料庫已初始化，共 {len(restaurants)} 間餐廳')
"
```

**方案 B：從 Google Places API 爬取**

```bash
# 確保 .env 中已填入 GOOGLE_PLACES_API_KEY
python scripts/sync_restaurants.py \
  --radius 1000 \
  --limit 50 \
  --lat 25.0330 \
  --lon 121.5654
```

#### 2.3 驗證資料庫

```bash
# 檢查資料庫檔案
ls -lh data/restaurants.db

# 查看資料表
sqlite3 data/restaurants.db ".tables"

# 查看資料筆數
sqlite3 data/restaurants.db "SELECT COUNT(*) FROM restaurants;"
```

✅ **檢查點**：確認 `data/restaurants.db` 存在且有資料

---

### **第 3 步：開發伺服器測試（30 分鐘）**

#### 3.1 啟動應用

```bash
# 啟動 Flask 開發伺服器
python src/main.py

# 預期輸出：
# * Running on http://localhost:5000
# * Debug mode: on
```

#### 3.2 測試健康檢查端點

```bash
# 另開一個終端，執行：
curl http://localhost:5000/health

# 預期回傳：
# {"status": "healthy", "db_count": 45, "version": "1.0.0"}
```

#### 3.3 測試抽籤 API

```bash
curl -X POST http://localhost:5000/api/lucky-draw \
  -H "Content-Type: application/json" \
  -d '{
    "distance_limit": 1000,
    "price_range": "mid",
    "require_mobile_payment": true
  }'

# 預期回傳：
# {
#   "restaurant": {
#     "name": "丸龜製麵",
#     "distance": 850,
#     "price_range": "mid",
#     "payment_methods": ["LINE Pay"],
#     "address": "台北市信義區...",
#     "maps_url": "https://maps.google.com/..."
#   }
# }
```

✅ **檢查點**：成功取得抽籤結果

---

### **第 4 步：LINE Bot 連接（45 分鐘）**

#### 4.1 LINE Developers 後台設定

1. 登入 [LINE Developers](https://developers.line.biz/)
2. 建立新的 Provider（提供者）
3. 在 Provider 下建立 Messaging API Channel
4. 進入 Channel 設定，找到：
   - **Channel Secret**：複製到 `.env` 的 `LINE_CHANNEL_SECRET`
   - **Channel Access Token**：複製到 `.env` 的 `LINE_CHANNEL_ACCESS_TOKEN`

#### 4.2 設定 Webhook URL

1. 在 LINE Developers 後台，找到「Webhook URL」
2. 填入：`http://localhost:5000/webhook/line`（本地測試）
3. 勾選「使用 Webhook」
4. 點擊「驗證」

#### 4.3 測試 LINE 訊息

1. 掃描 Channel QR Code 加入機器人
2. 在 LINE 傳送文字：`午餐` 或 `抽籤`
3. 機器人應回傳互動選單

✅ **檢查點**：LINE 成功收到回應

---

### **第 5 步：部署到雲端（1-1.5 小時）**

#### 5.1 部署前檢查

```bash
# 執行測試
pytest tests/ -v

# 代碼品質檢查
flake8 src/ --max-line-length=100

# 確認所有環境變數都填好
python -c "import os; from dotenv import load_dotenv; load_dotenv(); \
print('✅ 環境變數已加載' if os.getenv('LINE_CHANNEL_SECRET') else '❌ 缺少環境變數')"
```

#### 5.2 推送到 GitHub

```bash
git add .
git commit -m "Initial commit: AutoLunch LINE Bot architecture"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/autolunch.git
git push -u origin main
```

#### 5.3 部署到 Render（推薦）

1. 登入 [Render.com](https://render.com)
2. 點擊 New → Web Service
3. 連結 GitHub repo
4. 設定：
   - **Name**: autolunch
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT src.main:app`
5. 在 Environment Variables 中填入所有 `.env` 變數
6. Deploy 並等待部署完成

#### 5.4 更新 LINE Webhook URL

1. 複製 Render 應用的公開 URL（例如：`https://autolunch.onrender.com`）
2. 更新 LINE Developers 後台：
   - Webhook URL：`https://autolunch.onrender.com/webhook/line`
   - 驗證連接

#### 5.5 測試生產環境

```bash
# 測試健康檢查
curl https://YOUR_RENDER_APP.onrender.com/health

# 在 LINE 測試機器人
# 傳送「午餐」，確認回應
```

✅ **檢查點**：機器人在線上環境正常運作

---

## 📊 完成檢查清單

| 步驟 | 任務 | 完成 |
|------|------|------|
| 0 | 蒐集必要信息 | ☐ |
| 1 | 環境設定 | ☐ |
| 2 | 資料庫初始化 | ☐ |
| 3 | 本地測試 | ☐ |
| 4 | LINE 連接 | ☐ |
| 5 | 雲端部署 | ☐ |

---

## 🆘 常見問題排除

### 問題 1：`ModuleNotFoundError: No module named 'line'`
```bash
# 解決：重新安裝依賴
pip install line-bot-sdk
```

### 問題 2：`LINE Webhook 驗證失敗`
```bash
# 檢查：
# 1. LINE_CHANNEL_SECRET 是否正確複製
# 2. Webhook URL 是否完全正確
# 3. 伺服器是否正在運行
```

### 問題 3：`資料庫查詢無結果`
```bash
# 檢查資料庫是否有資料
sqlite3 data/restaurants.db "SELECT * FROM restaurants LIMIT 1;"

# 若無資料，執行初始化
python scripts/populate_sample_data.py
```

### 問題 4：`Google API 配額超出`
```bash
# 檢查使用量
# https://console.cloud.google.com/billing
# 升級免費額度或設定預警
```

---

## 📞 需要幫助？

- 查詢 [ARCHITECTURE.md](./ARCHITECTURE.md) 了解系統設計
- 查詢 [DATABASE_PLAN.md](./DATABASE_PLAN.md) 了解資料庫方案
- 聯絡：enchung_chang@cofit.me

---

**預計總時間**：4-6 小時  
**難度**：⭐⭐⭐（中等）  
**Last Updated**：2026-06-03
