# 🗺️ AutoLunch 開發路線圖

## 當前進度：第 1 步 ✅ 完成

### 已完成的文檔和決策

✅ **系統架構設計** → [ARCHITECTURE.md](./ARCHITECTURE.md)
- 整體架構圖
- 核心組件設計
- 業務流程圖
- 部署策略
- 開發時間預估：10-16 小時

✅ **資料庫方案評估** → [DATABASE_PLAN.md](./DATABASE_PLAN.md)
- 三大方案比較（Google Sheets vs SQLite vs PostgreSQL）
- **推薦方案**：SQLite（開發）+ PostgreSQL（生產）
- 推薦資料來源：Google Places API + 人工審核
- 維護策略與協作流程

✅ **快速開始指南** → [QUICK_START.md](./QUICK_START.md)
- 5 個主要步驟，完整的逐步教學
- 預計 4-6 小時從零到上線
- 每步驟都有驗證檢查點

---

## 🚀 立即行動（優先順序）

### 第 1 優先：蒐集必要信息（本週內）

**清單**：
- [ ] 確認公司地址 __(填入下方)__
  ```
  公司地址：_______________________
  經緯度：_______, _______
  ```

- [ ] 申請 Google Places API 金鑰（10 分鐘）
  1. 登入 [Google Cloud Console](https://console.cloud.google.com/)
  2. 建立新專案或選擇既有專案
  3. 啟用「Places API」和「Maps API」
  4. 建立 API 金鑰，複製到 `.env`

- [ ] 申請 LINE Developers 帳戶（10 分鐘）
  1. 登入 [LINE Developers](https://developers.line.biz/)
  2. 建立 Provider → Messaging API Channel
  3. 複製「Channel Secret」和「Channel Access Token」

### 第 2 優先：決定資料來源方案（本週內）

**兩種選擇**：

#### 選項 A：方案 A（推薦，自動化高）
- 用 Google Places API 自動爬取附近餐廳
- 人工標記「支援行動支付」的店家（需 0.5-1 小時）
- 自動化程度：80%
- 成本：$5/月 API 費用
- 維護難度：⭐

```bash
# 預計執行指令
python scripts/sync_restaurants.py --radius 1000 --lat YOUR_LAT --lon YOUR_LON
# 結果存入 CSV
# 人工在 Google Sheet 中標記支付方式
# 再匯入 SQLite
```

#### 選項 B：手動初始化示範資料
- 先用示範資料快速測試整個流程
- 之後再補充實際餐廳清單
- 自動化程度：0%
- 成本：0
- 維護難度：⭐⭐（需常手動更新）

```bash
# 直接執行
python scripts/populate_sample_data.py
# 立即可測試機器人
```

**建議**：選擇 **選項 A**（方案 A），時間成本低但長期受益高。

---

## 📅 週期計劃

### 第 1 週：基礎建設
- [ ] 完成上述「立即行動」清單
- [ ] 按 [QUICK_START.md](./QUICK_START.md) 完成環境設定
- [ ] 初始化資料庫（無論選 A 或 B）
- [ ] 啟動本地開發伺服器，測試健康檢查端點

**產出**：本地可運行的機器人框架

---

### 第 2 週：LINE Bot 連接 + 本地測試
- [ ] LINE Developers 後台設定
- [ ] 連接 Webhook URL
- [ ] 測試基本互動（傳送「午餐」，收到回應）
- [ ] 實現第一個 Flex Message 卡片

**產出**：可在 LINE 上互動的機器人

---

### 第 3 週：測試 + 優化
- [ ] 單元測試（距離計算、篩選邏輯）
- [ ] 集成測試（整個抽籤流程）
- [ ] Flex Message UI 優化（美化卡片外觀）
- [ ] 代碼審查 & 重構

**產出**：高質量、測試完善的代碼

---

### 第 4 週：部署 + 上線
- [ ] 推送代碼到 GitHub
- [ ] 部署到 Render（或 Zeabur）
- [ ] 線上環境測試
- [ ] 更新 LINE Webhook URL 至生產環境
- [ ] 邀請同事測試、收集反饋

**產出**：線上可用的機器人

---

## 💡 第 2 步預告

**下一步：LINE Developer 後台設定教學 + 代碼架構**

當你完成第 1 步的「立即行動」清單後，我會提供：

1. 📖 **LINE_SETUP_GUIDE.md**
   - 逐步的 LINE Developers 後台設定教學
   - 圖文並茂的操作流程
   - 常見問題排除

2. 🏗️ **核心代碼框架**
   - `src/main.py`：Flask 應用入口
   - `src/models/restaurant.py`：資料模型
   - `src/services/`：所有業務邏輯（距離計算、篩選、抽籤）
   - `src/handlers/line_handler.py`：LINE Webhook 處理
   - `src/database/`：資料庫操作層

3. 🎨 **Flex Message 範本**
   - 篩選選單卡片
   - 抽籤結果卡片
   - 導航按鈕整合

---

## 🎯 整體里程碑

```
Week 1: 環境建設 + 資料初始化
├─ 蒐集信息 + 申請 API 金鑰 ✅ 你現在在這
├─ 本地環境設定
├─ 資料庫初始化
└─ 本地伺服器測試

Week 2: LINE 連接 + 基本互動
├─ LINE 後台設定
├─ Webhook 連接
├─ 第一個回應訊息
└─ Flex Message 基礎

Week 3: 完善 + 測試
├─ 核心邏輯完善
├─ 單元 & 集成測試
├─ UI 優化
└─ 代碼審查

Week 4: 部署上線
├─ GitHub 版本管理
├─ Render 部署
├─ 線上測試
└─ 邀請同事內測

→ 🎉 AutoLunch v1.0 正式上線
```

---

## 📝 文檔導航

| 文檔 | 用途 | 何時閱讀 |
|------|------|--------|
| [README.md](./README.md) | 專案總覽 | 第一次接觸 |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 系統架構詳設 | 了解全貌時 |
| [DATABASE_PLAN.md](./DATABASE_PLAN.md) | 資料庫方案評估 | 決定資料來源時 |
| [QUICK_START.md](./QUICK_START.md) | 逐步操作指南 | 開始開發時 |
| [NEXT_STEPS.md](./NEXT_STEPS.md) | 路線圖 & 行動清單 | 現在 ← 你在這 |

---

## ❓ 常見疑問

### Q：為什麼把架構規劃這麼詳細放在第 1 步？
**A：** 充分規劃避免重工。一開始多花 30 分鐘理解架構，能省後期 5-10 小時的重構時間。

### Q：我可以跳過某些步驟嗎？
**A：** 不建議。建議按順序執行，每步都有驗證檢查點，確保穩定推進。

### Q：我想先自己試試看，不看代碼就做架構設計可以嗎？
**A：** 可以，但我已經為你準備好完整的設計和代碼框架。對新手來說，參考這套方案能加快 30% 的時間。

### Q：這個專案有多難？
**A：** 難度 ⭐⭐（中等偏易）。適合有 Python 基礎、想學 LINE Bot 開發的人。無需深度的 AI/機器學習知識。

---

## 🔗 外部資源

- 📚 [LINE Bot SDK 官方文檔](https://line-bot-sdk-python.readthedocs.io/)
- 🗺️ [Google Places API 文檔](https://developers.google.com/maps/documentation/places/web-service)
- 🐳 [Render 部署指南](https://render.com/docs)
- 📖 [Flask 官方教學](https://flask.palletsprojects.com/)

---

## ✉️ 反饋與支援

有任何疑問或建議，隨時聯絡：
- 📧 enchung_chang@cofit.me
- 💬 GitHub Issues（上線後）

---

**重要提醒**：

下一步前，請確保：
1. ✅ 已讀完 [QUICK_START.md](./QUICK_START.md)
2. ✅ 有 Google API 金鑰和 LINE Developers 帳戶
3. ✅ 確認公司經緯度
4. ✅ 決定資料來源方案（A 或 B）

**準備好了嗎？** 開始執行 QUICK_START.md 的第 1 步吧！🚀
