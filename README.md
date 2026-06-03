# 🍜 AutoLunch - LINE 午餐抽籤機器人

一個智能午餐推薦系統，幫助公司同事快速決定午餐去處。

## ✨ 核心功能

- 🎯 **距離篩選**：500m 或 1km 內的餐廳
- 💰 **預算分類**：平價、中價、高價三個級距
- 💳 **支付方式**：篩選支持行動支付的店家
- 🎲 **隨機抽籤**：一鍵產生午餐建議
- 🗺️ **導航連結**：直接連結 Google Maps

## 🛠️ 技術棧

| 組件 | 技術 |
|------|------|
| **後端** | Python 3.9+ + Flask / FastAPI |
| **資料庫** | SQLite（開發）/ PostgreSQL（生產） |
| **通訊** | LINE Messaging API v3 |
| **部署** | Render / Zeabur（免費方案） |
| **API** | Google Places API（資料來源） |

## 📋 專案結構

```
AutoLunch/
├── README.md                      # 專案說明（本檔）
├── ARCHITECTURE.md                # 系統架構詳細設計
├── DATABASE_PLAN.md               # 資料庫方案評估
├── requirements.txt               # Python 依賴清單
├── .env.example                   # 環境變數模板
│
├── src/
│   ├── __init__.py
│   ├── main.py                    # Flask/FastAPI 應用
│   ├── config.py                  # 配置管理
│   ├── models/                    # 資料模型
│   ├── services/                  # 業務邏輯服務
│   ├── handlers/                  # LINE 事件處理
│   ├── database/                  # 資料庫操作
│   └── utils/                     # 工具函數
│
├── data/
│   ├── restaurants.db             # SQLite 資料庫
│   └── restaurants_backup.csv     # 備份資料
│
├── scripts/
│   ├── sync_restaurants.py        # Google Places API 同步
│   └── populate_sample_data.py    # 示範資料初始化
│
└── tests/                         # 單元測試
```

## 🚀 快速開始

### 1️⃣ 前置需求

```bash
# 系統需求
- Python 3.9 或以上
- pip 或 conda 套件管理器

# 帳戶需求
- LINE Developers 帳戶（免費）
- Google Cloud Console 帳戶
- Render 或 Zeabur 帳戶（部署用）
```

### 2️⃣ 本地開發

```bash
# 複製專案
git clone https://github.com/你的帳號/autolunch.git
cd AutoLunch

# 建立虛擬環境
python -m venv venv
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate             # Windows

# 安裝依賴
pip install -r requirements.txt

# 設定環境變數
cp .env.example .env
# 編輯 .env，填入 LINE 和 Google API 金鑰
nano .env

# 初始化資料庫
python scripts/populate_sample_data.py

# 啟動開發伺服器
python src/main.py
# 伺服器運行在 http://localhost:5000
```

### 3️⃣ LINE Bot 設定

詳見：[LINE_SETUP_GUIDE.md](./docs/LINE_SETUP_GUIDE.md)

### 4️⃣ 部署到雲端

詳見：[DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md)

## 📊 資料庫初始化

### 方案 A：使用示範資料（快速測試）

```bash
python scripts/populate_sample_data.py
```

### 方案 B：從 Google Places API 爬取（推薦）

```bash
# 設定 Google API 金鑰於 .env
python scripts/sync_restaurants.py --radius 1000 --limit 50
```

### 方案 C：手動上傳 CSV

```bash
# restaurants.csv 欄位：name, latitude, longitude, price_range, payment_methods, address, phone
python scripts/import_csv.py --file restaurants.csv
```

## 🔧 使用者指南

### 用户端（LINE）

```
用户：午餐

機器人：請選擇篩選條件 [Flex Message 卡片]
       ├─ 距離：500m / 1km
       ├─ 預算：平價 / 中價 / 高價
       └─ 支付：全部 / 只限行動支付

用户：[點選「1km, 中價, 支持LINE Pay」]

機器人：🎉 抽籤結果 [Flex Message 卡片]
       ├─ 餐廳：麻辣火鍋
       ├─ 距離：850m（步行 11 分）
       ├─ 預算：¥200-300
       ├─ 支援：LINE Pay / 街口支付
       ├─ 評分：4.5 ⭐
       └─ [Google Maps 導航按鈕]
```

### 管理端（資料庫維護）

```bash
# 查看所有餐廳
python -c "from src.database.queries import list_all_restaurants; list_all_restaurants()"

# 新增餐廳
python scripts/add_restaurant.py --name "新餐廳" --lat 25.033 --lon 121.565

# 更新支付方式
python scripts/update_payment.py --restaurant "丸龜製麵" --payment "LINE Pay,街口支付"

# 刪除已結業餐廳
python scripts/deactivate_restaurant.py --name "已結業餐廳"
```

## 📈 系統監控

### 健康檢查端點

```bash
curl http://localhost:5000/health
# 回傳：{"status": "healthy", "db_count": 45, "version": "1.0.0"}
```

### 日誌查看

```bash
tail -f logs/app.log
```

## 🤝 協作維護

### Google Sheet 協作流程

1. 建立共用 Google Sheet：`AutoLunch 餐廳清單`
2. 欄位：名稱、座標、預算、支援支付方式、營業狀態、備註
3. 每月同步一次至 SQLite

```bash
python scripts/sync_from_gsheet.py --sheet-id YOUR_SHEET_ID
```

## 🧪 測試

```bash
# 執行所有單元測試
pytest tests/

# 執行特定測試
pytest tests/test_geometry.py -v

# 測試覆蓋率
pytest --cov=src tests/
```

## 📝 相關文檔

- [ARCHITECTURE.md](./ARCHITECTURE.md) - 系統架構設計
- [DATABASE_PLAN.md](./DATABASE_PLAN.md) - 資料庫方案評估
- [LINE_SETUP_GUIDE.md](./docs/LINE_SETUP_GUIDE.md) - LINE Developer 設定（開發中）
- [DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md) - 部署指南（開發中）
- [API_DOCS.md](./docs/API_DOCS.md) - API 文檔（開發中）

## 🐛 常見問題

### Q：為什麼資料庫用 SQLite 不用 PostgreSQL？
**A：** SQLite 適合開發和中小型應用。若用户超過 100 人且併發高，可升級到 PostgreSQL。

### Q：如何添加新的支付方式類別？
**A：** 編輯 `src/models/restaurant.py` 的 `PaymentMethod` Enum，重新啟動服務即可。

### Q：Google Places API 會不會很貴？
**A：** Google 免費額度 $200/月，足夠每月查詢 ~15,000 次。小於 100 家餐廳每月更新完全免費。

### Q：可以多個公司點位嗎？
**A：** 可以。編輯 `config.py` 的 `COMPANY_LOCATIONS` 列表，用户選擇時指定位置即可。

## 📧 支援與回饋

- 發現 Bug：GitHub Issues
- 功能建議：GitHub Discussions
- 直接聯絡：enchung_chang@cofit.me

## 📄 授權

MIT License - 詳見 [LICENSE](./LICENSE) 檔案

---

**Last Updated**: 2026-06-03  
**Maintainer**: Enchung Chang  
**Status**: 🟡 開發中（架構規劃完成，代碼開發中）
