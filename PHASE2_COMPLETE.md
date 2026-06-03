# ✅ 第 2 步完成：Python 代碼框架交付

**日期**：2026-06-03  
**狀態**：✅ 完整的 Python 代碼框架已編寫完成  
**代碼行數**：約 1,200+ 行  
**下一步**：啟動本地開發伺服器

---

## 📦 已交付的完整代碼

### 配置層

| 檔案 | 內容 |
|------|------|
| `src/config.py` | 應用配置管理（環境變數讀取、預設值） |

### 資料模型層

| 檔案 | 內容 |
|------|------|
| `src/models/restaurant.py` | 餐廳資料模型、Enum 定義 |

### 服務層（核心業務邏輯）

| 檔案 | 內容 | 功能 |
|------|------|------|
| `src/services/geometry_service.py` | 地理計算服務 | Haversine 距離公式、距離篩選 |
| `src/services/filter_service.py` | 篩選服務 | 價格篩選、支付方式篩選、綜合篩選 |
| `src/services/draw_service.py` | 抽籤服務 | 隨機抽籤、加權抽籤 |
| `src/services/navigation_service.py` | 導航服務 | Google Maps 連結生成 |

### 處理層

| 檔案 | 內容 | 功能 |
|------|------|------|
| `src/handlers/line_handler.py` | LINE 事件處理器 | 訊息接收、Flex Message 設計、事件回應 |

### 資料庫層

| 檔案 | 內容 | 功能 |
|------|------|------|
| `src/database/queries.py` | 資料庫查詢函數 | CRUD 操作、初始化 |

### 主應用

| 檔案 | 內容 | 功能 |
|------|------|------|
| `src/main.py` | Flask 應用入口 | 路由定義、Webhook 處理 |

### 初始化腳本

| 檔案 | 內容 | 功能 |
|------|------|------|
| `scripts/populate_sample_data.py` | 示範資料初始化 | 建立 8 間示範餐廳 |

---

## 🎯 代碼架構

```
AutoLunch 應用架構
═════════════════════════════════════════

User (LINE)
   ↓
[Flask 應用] ← main.py
   ↓
[LINE Webhook 處理] ← handlers/line_handler.py
   ├─ 文字訊息
   └─ Postback 事件
   ↓
[服務層] ← services/
   ├─ GeometryService (距離計算)
   ├─ FilterService (篩選邏輯)
   ├─ DrawService (隨機抽籤)
   └─ NavigationService (導航連結)
   ↓
[資料庫層] ← database/queries.py
   ↓
SQLite 資料庫
```

---

## 🚀 立即開始（5 分鐘）

### Step 1：安裝依賴

```bash
# 進入專案目錄
cd c:\Users\Enchung_Chang\Desktop\AutoLunch

# 確保虛擬環境已啟動
venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt
```

### Step 2：初始化資料庫

```bash
# 運行示範資料初始化腳本
python scripts/populate_sample_data.py
```

**預期輸出**：
```
初始化資料庫...
新增示範餐廳...
  ✅ [1/8] 丸龜製麵 (ID: 1)
  ✅ [2/8] 麻辣火鍋 (ID: 2)
  ...
✅ 成功新增 8 間示範餐廳！
```

### Step 3：啟動開發伺服器

```bash
# 啟動 Flask 伺服器
python src/main.py
```

**預期輸出**：
```
Starting AutoLunch Bot...
Company: 群健科技 Cofit
Location: 25.0638409, 121.5334954
Distance options: [300, 600, 1000, 1500]
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 4：在 LINE 上測試

1. 加入你的 LINE Bot（掃 QR Code）
2. 傳送「午餐」或「抽籤」
3. 機器人應該回傳篩選選單
4. 點擊選項，機器人應該回傳抽籤結果卡片

---

## ✨ 代碼特點

### 1️⃣ 清晰的架構分層

```
數據 ← 模型層 ← 服務層 ← 處理層 ← 應用
                                    ↑
                           (Flask 路由)
```

每層職責清晰，易於維護和擴展。

### 2️⃣ 完整的業務邏輯

```
抽籤流程：
用户輸入 → 參數驗證 → 距離篩選 → 價格篩選 → 支付方式篩選 → 隨機抽籤 → 生成結果卡片 → 回傳 LINE
```

### 3️⃣ 美觀的 Flex Message 設計

```
篩選選單卡片：
┌─────────────────────┐
│ 🍜 午餐抽籤        │
│ 選擇你的午餐條件吧！ │
│ 📍 距離:            │
│ [🚶 300m]          │
│ [🚶‍♂️ 600m]         │
│ [🚴 1km]           │
│ [🚴‍♂️ 1.5km]        │
└─────────────────────┘

結果卡片：
┌─────────────────────┐
│ 🎉 抽籤結果        │
│ 丸龜製麵            │
│ 距離：850m         │
│ 預算：💰          │
│ [📍 Google Maps]    │
└─────────────────────┘
```

### 4️⃣ 可擴展的設計

```
易於添加新功能：
- 添加新的篩選條件 → 在 FilterService 中添加方法
- 添加新的抽籤策略 → 在 DrawService 中添加方法
- 添加新的事件類型 → 在 line_handler.py 中添加處理器
```

---

## 📊 代碼統計

```
檔案數：        10 個
代碼行數：      1,200+ 行
功能函數：      30+ 個
類別：          5 個
Enum 類型：     2 個
```

---

## 🧪 測試餐廳清單

代碼已內建 8 間示範餐廳（全部在公司附近）：

1. 丸龜製麵 (日式烏龍麵) - 平價 - 支援 LINE Pay
2. 麻辣火鍋 (川式火鍋) - 中價 - 支援 LINE Pay
3. 時尚鐵板燒 (日式鐵板燒) - 高價 - 支援多種支付
4. 便當大王 (台灣便當) - 平價 - 現金
5. 義大利麵屋 (義式餐廳) - 中價 - 支援多種支付
6. 精選牛肉麵 (台灣牛肉麵) - 平價 - 支援 LINE Pay
7. 高檔壽司吧 (日式壽司) - 高價 - 支援多種支付
8. 港式茶餐廳 (港式餐廳) - 中價 - 現金

---

## 🔍 關鍵代碼摘要

### 距離計算（Haversine 公式）

```python
def haversine_distance(lat1, lon1, lat2, lon2):
    # 計算兩點間的實際距離（考慮地球曲率）
    # 結果：公尺
```

### 綜合篩選

```python
def apply_filters(restaurants, center_lat, center_lon, distance, 
                  price_ranges, require_mobile_payment):
    # 1. 篩選營業狀態
    # 2. 篩選距離
    # 3. 篩選價格
    # 4. 篩選支付方式
    # 結果：符合所有條件的餐廳列表
```

### 隨機抽籤

```python
def lucky_draw(restaurants):
    # 從篩選結果中隨機選一間
    return random.choice(restaurants)
```

### Flex Message 設計

```python
# 動態生成 Flex Message JSON
# 包含篩選選單和結果卡片
# 支援 LINE 最新的 Bubble 和 Box 元素
```

---

## ✅ 完成檢查清單

```
代碼交付完成清單
═════════════════════════════════════════

[x] 配置管理（config.py）
[x] 資料模型（models/）
[x] 地理計算服務（geometry_service.py）
[x] 篩選服務（filter_service.py）
[x] 抽籤服務（draw_service.py）
[x] 導航服務（navigation_service.py）
[x] LINE 事件處理（line_handler.py）
[x] 資料庫操作（database/queries.py）
[x] Flask 應用（main.py）
[x] 示範資料初始化（populate_sample_data.py）

✅ 所有代碼完成！準備測試！
```

---

## 🎯 下一步

### 立即（今天）

1. ✅ 安裝依賴
2. ✅ 初始化資料庫
3. ✅ 啟動伺服器
4. ✅ 在 LINE 上測試

### 本週

1. 測試各種篩選組合
2. 驗證距離計算准確性
3. 優化 Flex Message 設計
4. 收集反饋

### 下週

1. 修復 Bug
2. 性能優化
3. 添加更多餐廳資料
4. 準備部署

---

## 🎉 恭喜！

```
第 1 步：架構規劃 ✅ 完成
第 2 步：代碼框架 ✅ 完成

進度：50% 完成！

剩下：
├─ 本地測試（2-3 天）
├─ 功能優化（3-5 天）
└─ 部署上線（2-3 天）

預計 2-3 週內上線！
```

---

## 📞 需要幫助？

- **代碼有問題？** → 我會幫你修復
- **需要添加功能？** → 告訴我需求，我來編寫
- **測試遇到問題？** → 一起除錯

---

**現在就開始吧！** 🚀

```bash
cd c:\Users\Enchung_Chang\Desktop\AutoLunch
venv\Scripts\activate
pip install -r requirements.txt
python scripts/populate_sample_data.py
python src/main.py
```

在 LINE 上傳送「午餐」開始使用！

Last Updated: 2026-06-03
