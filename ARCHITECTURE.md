# AutoLunch LINE 午餐抽籤機器人 - 系統架構設計

## 📊 整體架構圖

```
┌─────────────────────────────────────────────────────────────────┐
│                     LINE Platform (Frontend)                     │
│              用户透過 LINE Bot 發起抽籤請求                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │ LINE Messaging API
                           │ (Webhook)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Backend Server (Python)                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐   │
│  │ LINE Webhook     │  │ Request Handler  │  │ Geocoding   │   │
│  │ Middleware       │  │ (篩選 & 距離計算)  │  │ (距離計算)   │   │
│  └──────────────────┘  └──────────────────┘  └─────────────┘   │
│           │                      │                    │          │
│           └──────────────────────┴────────────────────┘          │
│                           │                                      │
│                           ▼                                      │
│           ┌──────────────────────────────┐                       │
│           │  Core Logic Layer            │                       │
│           │  - 距離篩選 (Haversine)      │                       │
│           │  - 預算分類                   │                       │
│           │  - 隨機抽籤演算法            │                       │
│           └──────────────────────────────┘                       │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
    ┌─────────────────────┐ ┌──────────────────┐
    │ 餐廳資料庫          │ │ Google Maps API  │
    │ (SQLite/PostgreSQL) │ │ (導航連結生成)   │
    │ - 餐廳基本資訊      │ │                  │
    │ - 支付方式標記      │ └──────────────────┘
    │ - 座標/預算資訊     │
    └─────────────────────┘
```

---

## 🏗️ 核心架構組件

### 1. **前端（LINE Bot）**
- **接收端點**：Webhook 接收用户訊息
- **互動方式**：
  - 用户選擇篩選條件（距離、預算、支付方式）
  - 機器人顯示 Flex Message 卡片供互動
  - 實時反饋抽籤結果

### 2. **後端 API 層**
```
核心端點設計：
- POST /webhook/line          # 接收 LINE 訊息
- GET  /restaurants/search    # 搜尋餐廳（已廢棄，改用本地查詢）
- POST /restaurants/lucky-draw # 執行隨機抽籤
- GET  /health                # 健康檢查
```

### 3. **業務邏輯層（Core Logic）**
```python
核心功能模塊：
├── GeometryService
│   ├── haversine_distance()      # 計算兩點距離
│   └── filter_by_distance()      # 基於距離篩選
├── RestaurantFilter
│   ├── filter_by_price()         # 基於預算篩選
│   ├── filter_by_payment()       # 基於支付方式篩選
│   └── apply_all_filters()       # 綜合篩選
├── LuckyDrawService
│   ├── random_select()           # 隨機抽籤
│   └── format_result()           # 格式化結果
└── NavigationService
    └── generate_map_link()       # 生成 Google Maps 導航連結
```

### 4. **資料庫層**
儲存結構：
```sql
restaurants (
  id              INTEGER PRIMARY KEY
  name            TEXT            # 餐廳名稱
  latitude        FLOAT           # 緯度
  longitude       FLOAT           # 經度
  price_range     ENUM            # 平價/中價/高價
  cuisine_type    TEXT            # 菜系
  payment_methods TEXT            # 行動支付方式 (JSON)
  address         TEXT            # 完整地址
  phone           TEXT            # 電話
  rating          FLOAT           # 評分
  is_active       BOOLEAN         # 是否還在營業
  created_at      TIMESTAMP
  updated_at      TIMESTAMP
)
```

---

## 🗂️ 檔案結構設計

```
AutoLunch/
├── README.md                      # 專案說明
├── ARCHITECTURE.md                # 本文件
├── DATABASE_PLAN.md               # 資料庫選擇方案
├── .env.example                   # 環境變數模板
│
├── src/
│   ├── __init__.py
│   ├── main.py                    # Flask/FastAPI 應用入口
│   ├── config.py                  # 配置管理
│   │
│   ├── models/
│   │   └── restaurant.py          # 資料模型定義
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── geometry_service.py    # 地理計算服務
│   │   ├── filter_service.py      # 篩選邏輯
│   │   ├── draw_service.py        # 抽籤邏輯
│   │   └── navigation_service.py  # 導航連結生成
│   │
│   ├── handlers/
│   │   └── line_handler.py        # LINE Webhook 處理
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── init_db.py             # 資料庫初始化
│   │   └── queries.py             # 資料庫查詢操作
│   │
│   └── utils/
│       ├── logger.py              # 日誌工具
│       └── validators.py          # 輸入驗證
│
├── data/
│   ├── restaurants.db             # SQLite 資料庫（本地開發）
│   └── restaurants_backup.csv     # 備份資料
│
├── tests/
│   ├── __init__.py
│   ├── test_geometry.py           # 地理計算單元測試
│   ├── test_filters.py            # 篩選邏輯單元測試
│   └── test_integration.py        # 整合測試
│
├── scripts/
│   ├── sync_restaurants.py        # 從 Google Places API 同步餐廳
│   └── populate_sample_data.py    # 填入示範資料
│
├── requirements.txt               # Python 依賴
└── .gitignore
```

---

## 🔄 業務流程（User Flow）

### 抽籤流程圖
```
1. 用户在 LINE 輸入「午餐」或「抽籤」
   ▼
2. 機器人顯示篩選選單（Flex Message）
   - 距離選擇：500m / 1km
   - 預算選擇：平價 / 中價 / 高價
   - 支付方式：是否限定行動支付
   ▼
3. 用户提交篩選條件（Postback 事件）
   ▼
4. 後端執行篩選演算法
   - 從資料庫撈取所有餐廳
   - 基於用户輸入篩選（距離、預算、支付方式）
   - 計算每間餐廳與公司中心點的距離
   ▼
5. 隨機抽籤（從篩選結果中隨機選一間）
   ▼
6. 生成導航連結 + 格式化結果
   ▼
7. 回傳 Flex Message 卡片
   - 餐廳名稱、評分
   - 距離、預算範圍
   - 支援的行動支付方式
   - Google Maps 導航按鈕
   - 「重新抽籤」按鈕
```

---

## 🔐 API 安全性考慮

1. **LINE Signature 驗證**：驗證所有 Webhook 請求來自 LINE 官方
2. **Rate Limiting**：防止濫用（如 10 requests/min per user）
3. **輸入驗證**：驗證所有篩選條件參數
4. **環境變數管理**：敏感資訊（LINE Channel Secret/Access Token）不硬編碼

---

## 📈 效能考慮

1. **資料庫查詢最佳化**：
   - 對 `latitude`, `longitude`, `price_range` 建立索引
   - 使用分頁（若餐廳數量大）

2. **快取策略**：
   - 餐廳清單緩存（Redis 或記憶體快取）
   - 過期時間：1 小時

3. **距離計算優化**：
   - 使用 Haversine 公式計算，複雜度 O(n)
   - 對大規模資料可考慮 PostGIS 地理查詢

---

## 🚀 部署策略

### 開發階段
- **本地資料庫**：SQLite （方便快速迭代）
- **測試伺服器**：Render 免費方案

### 生產階段
- **資料庫**：PostgreSQL（Render 或 Railway）
- **應用伺服器**：Render 或 Zeabur（支援 Python）
- **成本估算**：完全免費～$10/月

---

## ⏱️ 開發時間預估

| 任務 | 時間 | 難度 |
|------|------|------|
| 資料庫設計 & 初始資料 | 2-4 小時 | ⭐ |
| 核心篩選邏輯 | 2-3 小時 | ⭐⭐ |
| LINE Webhook & 互動 | 2-3 小時 | ⭐⭐ |
| Flex Message UI 設計 | 1-2 小時 | ⭐ |
| 測試 & 除錯 | 2-3 小時 | ⭐⭐⭐ |
| 部署上線 | 1 小時 | ⭐ |
| **總計** | **10-16 小時** | |

