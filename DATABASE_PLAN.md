# AutoLunch - 資料庫方案評估與建議

## 📋 三大方案對比

### 方案比較表

| 指標 | Google Sheets | SQLite | PostgreSQL |
|------|------|--------|-----------|
| **初期成本** | 免費 | 免費 | 免費～$5/月 |
| **維護難度** | ⭐ (簡單) | ⭐⭐ | ⭐⭐⭐ |
| **查詢效能** | ⭐ (慢) | ⭐⭐⭐ (快) | ⭐⭐⭐⭐ (最快) |
| **併發支援** | ⭐ (不佳) | ⭐⭐ (單進程) | ⭐⭐⭐⭐⭐ |
| **規模上限** | ~10K 行 | ~100K 行 | 無上限 |
| **搜尋速度** | ~1-2 秒 | ~50ms | ~10ms |
| **地理查詢** | ❌ | ⭐⭐ (手動) | ⭐⭐⭐⭐ (GIS) |
| **自動化程度** | 低 | 中 | 高 |

---

## 🎯 推薦方案：**SQLite（開發） + PostgreSQL（生產）**

### 為什麼選 SQLite？

#### ✅ 優勢
1. **零部署難度**：單一 `.db` 檔案，複製即可
2. **開發效率**：本地快速迭代，無需設定資料庫伺服器
3. **足夠的容量**：100K+ 餐廳記錄無壓力
4. **查詢夠快**：距離篩選 50-100 家餐廳 <100ms
5. **容易備份**：整個 DB 就是一個檔案

#### ❌ 局限
- 寫入併發不佳（若同時 10+ 用户操作會有競爭）
- 無內建地理索引（距離計算需要應用層處理）

#### 何時升級到 PostgreSQL？
- 部署到生產環境且預期 >50 並發用户
- 需要 PostGIS 地理索引優化

---

## ❌ 為什麼不選 Google Sheets？

### 問題分析

```
❌ 查詢慢：
   Google Sheets API 每次查詢需要 HTTP 往返 (500-1000ms)
   若有 100 家餐廳，每次篩選都要等 0.5-1 秒

❌ 自動化困難：
   人工標記「支付方式」需要手動編輯 Sheet
   後續維護成本高（新餐廳需要人工審核）

❌ 併發問題：
   API 有 Rate Limit（每秒查詢數有限）
   多用户同時抽籤容易卡頓

❌ 無地理查詢：
   無內建距離計算功能，需要應用層逐筆計算
```

### 何時用 Google Sheets？
- **只適合**：初期資料來源（手動匯入到 SQLite）
- **用途**：非技術人員透過 Sheet 維護資料庫（定期同步到 SQLite）

---

## 💾 最終推薦架構

### 開發流程

```
第 0 步：資料準備
┌─────────────────────────────────────────┐
│ Google Places API（一次性）              │
│ - 爬取公司 1km 內的所有餐廳名稱           │
│ - 存入 CSV 或直接建 SQLite 初始資料       │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ 人工審核 + 標記行動支付方式              │
│ 選項 A: 用 Google Sheets 管理（推薦易用性）│
│ 選項 B: 直接編輯 SQLite 資料庫           │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ SQLite 資料庫（本地開發 + 部署）          │
│ - restaurants.db                        │
│ - 每晚定時更新（新增/刪除餐廳）          │
└─────────────────────────────────────────┘
```

### 部署流程

```
開發環境
├─ SQLite (restaurants.db)
├─ 本地測試

測試環境（Render）
├─ SQLite (上傳至 Render)
├─ 用戶驗收

生產環境（Render Premium 或 Railway）
├─ PostgreSQL (成本 $5-10/月)
├─ 備份策略
└─ 監控告警
```

---

## 🗄️ 資料庫 Schema（SQLite）

```sql
CREATE TABLE restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    
    -- 分類
    cuisine_type TEXT,                   -- 菜系（中式、日式、義式等）
    price_range TEXT NOT NULL,           -- 平價、中價、高價
    
    -- 支付方式 (JSON 格式，方便擴展)
    payment_methods TEXT,                -- ["LINE Pay", "街口支付"]
    accepts_mobile_payment BOOLEAN,      -- 快速查詢用
    
    -- 聯絡資訊
    address TEXT,
    phone TEXT,
    google_maps_url TEXT,
    
    -- 評分
    rating FLOAT DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    
    -- 營業狀態
    is_active BOOLEAN DEFAULT TRUE,
    last_verified_date DATETIME,         -- 上次人工確認時間
    
    -- 時間戳
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 索引優化
    INDEX idx_distance (latitude, longitude),
    INDEX idx_price (price_range),
    INDEX idx_payment (accepts_mobile_payment),
    INDEX idx_active (is_active)
);

-- 支付方式清單（正規化表）
CREATE TABLE payment_methods (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    icon_url TEXT
);
INSERT INTO payment_methods (name, icon_url) VALUES
('LINE Pay', 'https://...'),
('街口支付', 'https://...'),
('Apple Pay', 'https://...'),
('Google Pay', 'https://...');
```

---

## 📊 初期資料來源策略

### 步驟 1：Google Places API 爬取（建議用 Python 腳本）

```python
# 示範流程（實際代碼見後續章節）
from google.maps import Client

maps_client = Client(key='YOUR_API_KEY')

# 搜尋公司 1km 內的所有餐廳
places_result = maps_client.places_nearby(
    location=(25.0330, 121.5654),  # 台灣為例
    radius=1000,
    type='restaurant'
)

# 結果存入 CSV
# 欄位：名稱、座標、地址、評分、營業時間
```

### 步驟 2：人工標記行動支付（Google Sheets 或本地標記）

| 餐廳名稱 | 座標 | LINE Pay | 街口 | Apple Pay | 說明 |
|---------|------|---------|------|-----------|------|
| 丸龜製麵 | 25.03, 121.56 | ✅ | ❌ | ❌ | 官方 APP 確認 |
| 麻辣火鍋 | 25.04, 121.57 | ❌ | ✅ | ⚠️ | Google 評論提及 |

### 步驟 3：導入 SQLite

```python
# 自動化導入 Google Sheet 或 CSV 到 SQLite
import pandas as pd
import sqlite3

df = pd.read_csv('restaurants_marked.csv')
conn = sqlite3.connect('restaurants.db')
df.to_sql('restaurants', conn, if_exists='append')
```

---

## 🔄 維護策略

### 定期更新流程

| 時間 | 任務 | 負責 |
|------|------|------|
| 每月 | 驗證餐廳是否還在營業 | 一位同事 |
| 每月 | 新增/刪除餐廳 | 群組協作 |
| 每月 | 更新 Google Maps 評分 | 自動化腳本 |

### 協作方案

#### 方案 A：純 SQLite（推薦技術人員）
```
編輯 restaurants.db → Git 版控 → 部署
```

#### 方案 B：Google Sheet 作中介
```
Google Sheet（非技術人員編輯）
  ↓
Python 腳本（每天定時同步）
  ↓
SQLite 資料庫（應用層查詢）
```

---

## 💡 關鍵決策

### 推薦方案：**方案 A（Google Places API 爬取 + 人工審核）**

**理由**：
1. ✅ **成本低**：只需 Google Places API（$7/1000 次查詢，月成本 <$5）
2. ✅ **自動化高**：初始資料自動撈取，之後只需人工補充支付方式
3. ✅ **長期可維護**：可寫月度更新腳本自動同步新餐廳
4. ✅ **數據準確**：評分、評論數等自動更新

**實施步驟**：
```
Week 1: Google Places API 爬取 + 初步 CSV
Week 2: 人工標記支付方式 + 驗證資料正確性
Week 3: 導入 SQLite + 編寫維護腳本
Week 4: 部署到 Render
```

### 不推薦方案 B 的原因

**方案 B（Google Maps 評論爬蟲分析支付關鍵字）**

```
❌ 技術複雜度高：
   - 需要 NLP 模型判斷評論中的支付方式提及
   - 準確度不高（評論可能提「LINE」但不是支付）
   - 爬蟲易被 Google 限制

❌ 時間成本：
   - 開發 3-5 倍時間
   - 維護難度高

✅ 唯一優勢：完全自動化
   - 但人工標記其實也不費時（50 家餐廳 <30 分鐘）
```

---

## 🎯 最終決策矩陣

```
需求               →  推薦方案
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
快速上線           →  SQLite + 方案 A
成本考量           →  SQLite + 方案 A（Google API $5/月）
易於維護           →  SQLite + Google Sheet 協作
技術挑戰           →  方案 B（不推薦，時間成本高）
未來擴展           →  PostgreSQL（若用户>100人）
```

---

## 📌 下一步行動清單

- [ ] 確認公司地址/經緯度
- [ ] 申請 Google Places API（免費 $200 月度額度足夠）
- [ ] 決定資料維護方式（純 SQLite vs Google Sheet 中介）
- [ ] 收集公司同事對「常去餐廳」的偏好清單
- [ ] 第一批資料爬取 & 人工審核（預計 2-4 小時）

