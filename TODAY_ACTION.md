# 🎯 今天立即行動清單

**日期**：2026-06-03  
**進度**：✅ 第 1 步完成 → 📍 第 2 步開始  
**預計時間**：2-3 小時

---

## ⏰ 優先順序

### 🔴 最高優先（必須今天完成）

#### 1️⃣ **LINE Developers 後台設定**（15 分）

**步驟**：
1. 登入 https://developers.line.biz/
2. 建立新的 Provider（提供者名稱：`AutoLunch`）
3. 在 Provider 下建立 Messaging API Channel
   - Channel name：`AutoLunch Bot`
   - Channel description：`GROUP LUNCH LOTTERY BOT`
4. 進入 Channel 設定，複製：
   - `Channel Secret` ✅
   - `Channel Access Token` ✅

**複製這兩個值後，貼到下面**：
```
LINE_CHANNEL_SECRET = ___________________
LINE_CHANNEL_ACCESS_TOKEN = ___________________
```

---

#### 2️⃣ **Google Cloud 設定**（10 分）

**步驟**：
1. 登入 https://console.cloud.google.com/
2. 建立新專案：`AutoLunch`
3. 啟用以下 API：
   - ✅ Places API
   - ✅ Maps API
4. 建立 API 金鑰
5. 複製 API 金鑰

**複製後貼到下面**：
```
GOOGLE_MAPS_API_KEY = ___________________
GOOGLE_PLACES_API_KEY = ___________________
```

---

#### 3️⃣ **編輯 .env 檔案**（5 分）

**在你的 AutoLunch 資料夾中**：
1. 打開 `.env` 檔案（若無，複製 `.env.example`）
2. 填入上面複製的值：

```bash
# LINE Bot Configuration
LINE_CHANNEL_SECRET=你的 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN=你的 Access Token

# Google APIs Configuration
GOOGLE_MAPS_API_KEY=你的 API Key
GOOGLE_PLACES_API_KEY=你的 API Key
```

3. **保存檔案**

✅ **完成！** 環境變數已設定。

---

### 🟠 高優先（今天內完成）

#### 4️⃣ **等待我的代碼框架**

我會在今天提供：
- [ ] Python 代碼框架（`src/` 資料夾）
- [ ] Flex Message 範本（JSON 設計）
- [ ] LINE_SETUP_GUIDE.md（詳細教學）
- [ ] 資料庫初始化腳本

**你只需等待**，無需做任何事。

---

### 🟡 中優先（明天開始）

#### 5️⃣ **設定 Webhook URL**

**等我提供代碼後**：
1. 啟動本地開發伺服器：`python src/main.py`
2. 在 LINE Developers 後台設定：
   - Webhook URL：`http://localhost:5000/webhook/line`
3. 點擊「驗證」

---

#### 6️⃣ **本地測試**

**安裝依賴後**：
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

**在 LINE 上測試**：
- 加入你的 Bot
- 傳送「午餐」或「抽籤」
- 確認機器人有回應

---

## 📋 今日檢查清單

```
今日任務（2026-06-03）
═════════════════════════════════════════

□ LINE Developers 設定
  □ 建立 Provider
  □ 建立 Messaging API Channel
  □ 複製 Channel Secret ✅
  □ 複製 Access Token ✅

□ Google Cloud 設定
  □ 建立專案
  □ 啟用 Places API ✅
  □ 啟用 Maps API ✅
  □ 建立 API 金鑰 ✅

□ 編輯 .env 檔案
  □ 填入 LINE_CHANNEL_SECRET ✅
  □ 填入 LINE_CHANNEL_ACCESS_TOKEN ✅
  □ 填入 GOOGLE_MAPS_API_KEY ✅
  □ 填入 GOOGLE_PLACES_API_KEY ✅
  □ 保存檔案 ✅

□ 等待我的代碼框架
  □ Python 代碼（src/）
  □ Flex Message 範本
  □ LINE_SETUP_GUIDE.md

✅ 全部完成？ → 明天開始本地測試！
```

---

## ⏱️ 時間估算

| 任務 | 時間 |
|------|------|
| LINE Developers 設定 | 15 分 |
| Google Cloud 設定 | 10 分 |
| 編輯 .env | 5 分 |
| 等待代碼 | 0 分（我在做） |
| **總計** | **30 分** |

---

## 🎯 關鍵信息

### ✅ 你今天只需做 3 件事

1. **LINE 後台** → 複製 Secret & Token
2. **Google 後台** → 複製 API 金鑰
3. **編輯 .env** → 填入上述值

### ✅ 我今天會做的

1. **編寫 Python 代碼框架**
   - `src/main.py` - Flask 應用
   - `src/models/` - 資料模型
   - `src/services/` - 業務邏輯
   - `src/handlers/` - LINE 事件處理
   - `src/database/` - 資料庫操作

2. **設計 Flex Message**
   - 篩選選單卡片
   - 抽籤結果卡片

3. **編寫教學**
   - LINE_SETUP_GUIDE.md
   - 代碼註解

### ✅ 我們一起做的

- 本地測試（明天）
- Bug 修復和優化（整個開發周期）
- 部署上線（Week 4）

---

## 🔗 快速連結

| 服務 | 連結 |
|------|------|
| LINE Developers | https://developers.line.biz/ |
| Google Cloud Console | https://console.cloud.google.com/ |
| 你的 GitHub | https://github.com/matel5816-ux/autolunch |
| AutoLunch 資料夾 | `c:\Users\Enchung_Chang\Desktop\AutoLunch` |

---

## 💬 完成後回報

當你完成上述 3 件事後，告訴我：

```
✅ LINE Developers 設定完成
✅ Google API 金鑰已複製
✅ .env 檔案已填入

準備開始開發！
```

我會立即提供代碼框架和 LINE 設定指南。

---

## 🚀 下一步時間表

```
今天（2026-06-03）
└─ 你：LINE + Google 設定（30 分）
   我：代碼框架（同時進行）

明天（2026-06-04）
└─ 我：交付代碼 + 教學
   你：本地環境設定（30 分）

後天（2026-06-05）
└─ 你：本地測試（1-2 小時）
   我：修復 Bug（邊測邊修）

下週
└─ 資料庫初始化 + 功能完善
   └─ 逐週推進直到上線
```

---

## ❓ 常見問題

### Q：我沒有信用卡可以申請 Google API 嗎？
**A：** Google 給每個新帳戶 $300 免費額度，無需信用卡（但需驗證）。如需要，我們可以用免費額度，足夠 3-6 個月使用。

### Q：我可以先不設定 Google API 嗎？
**A：** 可以，先用示範資料測試。但如果你想真實爬取附近餐廳，需要 Google API。

### Q：LINE Bot 需要付費嗎？
**A：** 不需要。LINE Messaging API 對開發者免費，沒有費用。

### Q：我設定錯了怎麼辦？
**A：** 沒關係，可以隨時重新設定或刪除重建。我會提供詳細的除錯指南。

---

## 📞 需要幫助？

- **LINE 設定卡住**？→ 稍等，我會提供詳細教學
- **Google API 問題**？→ 提供截圖給我，我來幫你除錯
- **.env 編輯有問題**？→ 我會提供範本
- **其他技術問題**？→ 隨時提問

---

**🎉 準備好了嗎？開始這 3 件事吧！**

完成後告訴我，我會立即提供代碼框架。

**預計明天上午**就能交付完整的 Python 代碼！ 🚀

Good luck! 💪
