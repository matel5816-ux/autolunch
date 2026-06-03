# 📋 後續任務分配表

**完成狀態**：✅ 第 1 步已完成（架構規劃 + GitHub 推送）  
**現在進度**：📍 第 2 步準備開始  
**預計時間**：2-4 週（Week 1-4）

---

## 🎯 任務分配原則

| 誰做 | 任務類型 | 例子 |
|------|--------|------|
| **我（Claude）** | 💻 代碼編寫、架構設計、測試 | 寫 Python 代碼、設計 Flex Message、編寫測試 |
| **你（開發者）** | 🔐 需認證的操作、外部服務申請、測試驗證 | LINE 後台設定、Google API 配置、上線驗收 |
| **自動化** | 🤖 部署、監控、更新 | Render 部署、GitHub Actions CI/CD |

---

## 📅 第 2 步：LINE Developer 設定 + 核心代碼框架（Week 1-2）

### 你需要做的部分 👤

| 任務 | 難度 | 時間 | 說明 |
|------|------|------|------|
| **1. LINE Developers 後台設定** | ⭐ | 15 分 | 建立 Channel、取得 Secret & Access Token |
| **2. 獲取 Google API 金鑰** | ⭐ | 10 分 | Google Cloud Console 申請 Places API 金鑰 |
| **3. 編輯 .env 檔案** | ⭐ | 5 分 | 填入 LINE_CHANNEL_SECRET、LINE_CHANNEL_ACCESS_TOKEN、Google API Key |
| **4. 測試 Webhook 連接** | ⭐⭐ | 20 分 | 驗證 LINE Bot 能否收到訊息 |
| **5. 用 LINE 測試機器人** | ⭐ | 20 分 | 加入 Bot、傳送「午餐」指令、驗證回應 |

### 我能幫你做的部分 💻

| 任務 | 內容 | 交付物 |
|------|------|--------|
| **1. Python 代碼框架** | 編寫 Flask 應用架構、數據模型、業務邏輯 | `src/main.py`、`src/models/`、`src/services/` |
| **2. LINE Webhook 處理器** | 編寫 LINE 訊息接收、事件處理、回應邏輯 | `src/handlers/line_handler.py` |
| **3. 地理計算服務** | 實現 Haversine 距離公式、餐廳篩選邏輯 | `src/services/geometry_service.py` |
| **4. Flex Message 範本** | 設計互動卡片（篩選選單、抽籤結果） | Flex Message JSON 範本 |
| **5. 資料庫操作層** | 編寫 SQLite 查詢、初始化腳本 | `src/database/`、`scripts/` |
| **6. 第一版代碼骨架** | 整合上述組件，確保可以啟動 | 完整可運行的代碼 |

---

## 📅 第 3 步：功能測試與優化（Week 2-3）

### 你需要做的部分 👤

| 任務 | 難度 | 時間 | 說明 |
|------|------|------|------|
| **1. 本地測試** | ⭐⭐ | 2-3 小時 | 啟動伺服器，在 LINE 上測試各種篩選組合 |
| **2. 資料庫初始化** | ⭐ | 1 小時 | 從 Google Places API 爬取餐廳、人工標記支付方式 |
| **3. 測試不同距離選項** | ⭐ | 30 分 | 驗證 300m、600m、1km、1.5km 篩選是否準確 |
| **4. Bug 報告** | ⭐ | 邊測邊報 | 發現問題時告訴我（我負責修復） |

### 我能幫你做的部分 💻

| 任務 | 內容 | 交付物 |
|------|------|--------|
| **1. 單元測試** | 編寫距離計算、篩選邏輯的測試 | `tests/test_geometry.py`、`tests/test_filters.py` |
| **2. 集成測試** | 測試完整的抽籤流程 | `tests/test_integration.py` |
| **3. Bug 修復** | 你報告 → 我修復 → 你驗證 | 修復後的代碼 + 推送到 GitHub |
| **4. 性能優化** | 優化查詢速度、減少響應延遲 | 更快的代碼 |
| **5. Flex Message 優化** | 美化卡片、改進使用者體驗 | 更美觀的卡片設計 |

---

## 📅 第 4 步：部署上線（Week 3-4）

### 你需要做的部分 👤

| 任務 | 難度 | 時間 | 說明 |
|------|------|------|------|
| **1. Render 帳戶申請** | ⭐ | 5 分 | 前往 render.com 申請免費帳戶 |
| **2. 連接 GitHub 到 Render** | ⭐⭐ | 15 分 | Render 後台設定 GitHub 授權 |
| **3. 配置環境變數** | ⭐ | 10 分 | 在 Render 後台填入 LINE Secret 等敏感信息 |
| **4. 部署應用** | ⭐ | 5 分 | 點擊部署按鈕，等待完成 |
| **5. 更新 LINE Webhook URL** | ⭐ | 10 分 | LINE Developers 後台改為 Render 的 URL |
| **6. 線上測試** | ⭐⭐ | 30 分 | 在 LINE 上測試線上版本是否正常 |
| **7. 邀請內測** | ⭐ | 邊測邊邀 | 邀請公司同事測試、收集反饋 |

### 我能幫你做的部分 💻

| 任務 | 內容 | 交付物 |
|------|------|--------|
| **1. Render 部署指南** | 編寫詳細的部署步驟文檔 | `DEPLOYMENT_GUIDE.md` |
| **2. 生產環境配置** | 優化代碼以適應雲端環境 | 優化後的代碼 |
| **3. 監控與日誌** | 設置錯誤追蹤、日誌系統 | Sentry / Loki 整合 |
| **4. CI/CD 設置** | 編寫 GitHub Actions 自動部署流程 | `.github/workflows/deploy.yml` |
| **5. 故障排除** | 部署過程中的任何問題 | 快速修復 |

---

## 🔄 完整流程圖

```
Week 1：環境建設
├─ 你：LINE Developers 設定 (15 分)
├─ 我：編寫 Python 代碼框架
├─ 你：填入 API 金鑰 (5 分)
├─ 我：編寫 Flex Message 範本
└─ 你：本地測試 (20 分) → 報告 Bug

Week 2：功能完善
├─ 你：資料庫初始化 (1 小時)
├─ 我：修復 Bug + 優化代碼
├─ 你：再次測試 (2-3 小時) → 報告反饋
└─ 我：性能優化 + UI 美化

Week 3：準備部署
├─ 你：申請 Render 帳戶 (5 分)
├─ 我：編寫部署指南 + 優化代碼
├─ 你：連接 GitHub 到 Render (15 分)
└─ 我：設置 CI/CD

Week 4：上線驗證
├─ 你：部署應用 (5 分) + 線上測試 (30 分)
├─ 我：監控系統、快速修復問題
├─ 你：邀請同事內測、收集反饋
└─ 🎉 正式上線！
```

---

## 📝 具體下一步（立即開始）

### 今天（第 2 步第 1 天）- 2-3 小時

#### 你需要做的：

1. **LINE Developers 後台設定**（15 分）
   - [ ] 前往 https://developers.line.biz/
   - [ ] 建立新 Provider（提供者）
   - [ ] 在 Provider 下建立 Messaging API Channel
   - [ ] 複製 Channel Secret 和 Access Token
   - 📄 我會提供詳細教學：[LINE_SETUP_GUIDE.md]（待編寫）

2. **Google Cloud Console 設定**（10 分）
   - [ ] 前往 https://console.cloud.google.com/
   - [ ] 建立新專案
   - [ ] 啟用 Places API 和 Maps API
   - [ ] 建立 API 金鑰

3. **填入環境變數**（5 分）
   ```bash
   # 編輯 .env 檔案
   nano .env
   
   # 填入以下內容：
   LINE_CHANNEL_SECRET=你從LINE複製的
   LINE_CHANNEL_ACCESS_TOKEN=你從LINE複製的
   GOOGLE_MAPS_API_KEY=你從Google複製的
   GOOGLE_PLACES_API_KEY=你從Google複製的
   ```

#### 我會為你做的：

1. **編寫完整 Python 代碼框架**（今天交付）
   - ✅ `src/main.py` - Flask 應用入口
   - ✅ `src/models/restaurant.py` - 資料模型
   - ✅ `src/services/geometry_service.py` - 地理計算
   - ✅ `src/services/filter_service.py` - 篩選邏輯
   - ✅ `src/handlers/line_handler.py` - LINE 事件處理
   - ✅ `src/database/queries.py` - 資料庫操作

2. **編寫 Flex Message 範本**（今天交付）
   - ✅ 距離篩選卡片
   - ✅ 預算篩選卡片
   - ✅ 支付方式卡片
   - ✅ 抽籤結果卡片

3. **編寫詳細教學**（今天交付）
   - ✅ LINE_SETUP_GUIDE.md - LINE 後台設定步驟
   - ✅ 代碼文檔和註解

---

## 🎯 預期時間表

| 階段 | 你的工作量 | 我的工作量 | 時間 |
|------|-----------|-----------|------|
| Week 1：環境建設 | 2-3 小時 | 6-8 小時 | 3-5 天 |
| Week 2：功能完善 | 2-3 小時 | 4-6 小時 | 3-5 天 |
| Week 3：準備部署 | 1 小時 | 2-3 小時 | 2-3 天 |
| Week 4：上線驗證 | 1-2 小時 | 1-2 小時 | 2-3 天 |
| **總計** | **6-8 小時** | **13-19 小時** | **2-4 週** |

---

## 📊 技能分配

### 你的角色（開發者）
- ✅ 需要申請/配置的服務（LINE、Google API、Render）
- ✅ 測試和驗證（本地測試、線上測試）
- ✅ 內測和反饋收集
- ✅ 部署後的維護和監控

### 我的角色（技術顧問 + 開發者）
- ✅ 編寫所有 Python 代碼
- ✅ 設計系統架構和業務邏輯
- ✅ 編寫文檔和教學
- ✅ 修復 Bug 和優化性能
- ✅ 設計使用者介面（Flex Message）
- ✅ 部署和監控配置

---

## 🚀 立即開始第 2 步

### 任務清單：

```
□ 1. LINE Developers 後台設定（15 分）
     → 我會提供 LINE_SETUP_GUIDE.md

□ 2. Google Cloud 設定（10 分）
     → 參考 QUICK_START.md 的說明

□ 3. 填入 .env（5 分）
     → 複製 .env.example → 編輯 .env

□ 4. 等待我的代碼框架（今天交付）
     → 我會編寫 src/ 下的所有代碼
     → 提供 Flex Message 範本
     → 編寫詳細的 LINE_SETUP_GUIDE

✅ 完成上述後，進行第一次本地測試
```

---

## 🆘 需要幫助？

- **LINE 設定問題**？→ 等我提供 `LINE_SETUP_GUIDE.md`
- **Google API 問題**？→ 我會加入設定指南
- **代碼相關**？→ 所有代碼由我編寫和維護
- **測試和除錯**？→ 我會提供單元測試和修復 Bug
- **部署問題**？→ 我會提供 `DEPLOYMENT_GUIDE.md`

---

## ✅ 簽署

**開發者**：你  
**技術顧問 + 開發者**：Claude Code Assistant  

**合作模式**：
- 你負責外部服務申請和測試驗證
- 我負責代碼編寫和系統設計
- 我們一起打造 AutoLunch！

---

**準備好了嗎？** 👉 開始第 2 步！

我會立即開始編寫代碼框架和教學文檔。

**預計交付時間**：今天 (2026-06-03)

🚀 Let's build AutoLunch together!
