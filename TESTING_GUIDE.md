# 🧪 完整測試指南

**目標**：在本地啟動 AutoLunch Bot，透過 LINE 進行完整測試

**預計時間**：20-30 分鐘

---

## 📋 測試前準備

### 檢查清單

```
□ .env 檔案已配置（LINE Secret 和 Token）
□ 虛擬環境已啟動（venv\Scripts\activate）
□ 依賴已安裝（pip install -r requirements.txt）
□ 示範資料已初始化（python scripts/populate_sample_data.py）
□ 你的 LINE Bot 已建立（https://developers.line.biz/）
```

---

## 🚀 步驟 1：啟動開發伺服器

### 1.1 打開終端

```bash
# 進入專案目錄
cd c:\Users\Enchung_Chang\Desktop\AutoLunch

# 啟動虛擬環境
venv\Scripts\activate

# 應該看到這樣的提示：
# (venv) C:\Users\Enchung_Chang\Desktop\AutoLunch>
```

### 1.2 啟動 Flask 伺服器

```bash
python src/main.py
```

### 1.3 確認伺服器啟動成功

**預期輸出**：
```
Starting AutoLunch Bot...
Company: 群健科技 Cofit
Location: 25.0638409, 121.5334954
Distance options: [300, 600, 1000, 1500]
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

✅ **如果看到上述訊息，表示伺服器已成功啟動！**

⚠️ **如果出現錯誤**：
- 檢查 .env 檔案是否正確配置
- 確認依賴是否安裝完整
- 嘗試刪除 `data/restaurants.db`，重新執行初始化腳本

---

## 🔗 步驟 2：設定 LINE Webhook URL（本機測試）

### ⚠️ 重要：本機測試的特殊步驟

由於我們在本地開發，LINE 無法直接訪問你的電腦。我們需要使用 **ngrok** 或 **localtunnel** 來建立公開的 HTTPS 連結。

### 選項 A：使用 ngrok（推薦）

#### 2.1 安裝 ngrok

1. 前往 https://ngrok.com/
2. 下載 ngrok（Windows 版本）
3. 解壓縮到一個資料夾（例如 `C:\ngrok`）

#### 2.2 啟動 ngrok

打開新的終端（不要關閉 Flask 伺服器那個）：

```bash
# 進入 ngrok 資料夾
cd C:\ngrok

# 啟動 ngrok（將本機 5000 port 轉發到公開 HTTPS）
ngrok http 5000
```

**預期輸出**：
```
ngrok by @inconshreveable

Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                        ap (Asia Pacific)
Latency                       45ms
Web Interface                 http://127.0.0.1:4040

Forwarding                    https://xxxx-xx-xxx-xxx.ngrok.io -> http://localhost:5000
```

✅ **複製這個 HTTPS 網址**：`https://xxxx-xx-xxx-xxx.ngrok.io`

#### 2.3 在 LINE Developers 設定 Webhook URL

1. 登入 LINE Developers 後台：https://developers.line.biz/
2. 找到你的 Channel 設定
3. 找到「Webhook URL」輸入框
4. 填入：`https://xxxx-xx-xxx-xxx.ngrok.io/webhook/line`（用上面複製的網址）
5. 點「保存」

### 選項 B：簡單測試（不設定 Webhook）

如果你不想用 ngrok，也可以先跳過 Webhook 設定，用以下方式測試：

```bash
# 直接用 curl 測試 API
curl http://localhost:5000/health
```

應該看到：
```json
{
  "status": "healthy",
  "service": "AutoLunch LINE Bot",
  "version": "1.0.0"
}
```

---

## 💬 步驟 3：在 LINE 上測試

### 3.1 加入你的 LINE Bot

1. 登入 LINE Developers 後台
2. 找到你的 Channel
3. 掃描 QR Code 加入 Bot
   或
   搜尋 Bot 的 ID 加入

### 3.2 開始測試

#### 測試 1️⃣：基本對話

**你傳送**：
```
午餐
```

**期望的回應**：
- Bot 應該回傳一個 Flex Message 卡片
- 卡片顯示「🍜 午餐抽籤」
- 顯示四個距離按鈕：300m, 600m, 1km, 1.5km

✅ **驗證**：能否看到選單卡片

---

#### 測試 2️⃣：距離篩選

**你點擊**：`🚴 1km (13-15分鐘)` 按鈕

**期望的回應**：
- Bot 進行抽籤
- 回傳一個結果卡片，顯示：
  - 🎉 抽籤結果
  - 餐廳名稱（例如：丸龜製麵）
  - 距離（例如：850m）
  - 預算（例如：💰 budget）
  - [📍 Google Maps] 導航按鈕

✅ **驗證**：
- 距離是否合理（應該 < 1000m）
- 餐廳名稱是否正確
- Google Maps 連結是否可點擊

---

#### 測試 3️⃣：不同距離選項

**分別點擊以下按鈕，檢查結果距離**：

| 按鈕 | 預期距離 | 測試結果 |
|------|---------|---------|
| 300m | < 300m | ✅ / ❌ |
| 600m | < 600m | ✅ / ❌ |
| 1km | < 1000m | ✅ / ❌ |
| 1.5km | < 1500m | ✅ / ❌ |

✅ **驗證**：所有距離篩選是否准確

---

#### 測試 4️⃣：多次抽籤

**重複點擊多次**（例如 5 次），檢查是否每次都有不同的結果

✅ **驗證**：
- 不是每次都抽到同一間餐廳
- 抽籤有隨機性

---

#### 測試 5️⃣：Google Maps 導航

**點擊結果卡片中的 [📍 Google Maps] 按鈕**

✅ **驗證**：
- 是否能打開 Google Maps
- 位置是否正確（應該在台北中山區）
- 顯示的餐廳位置是否合理

---

## 🐛 步驟 4：除錯和日誌查看

### 4.1 查看伺服器日誌

在啟動 Flask 伺服器的終端中，你應該能看到：

```
127.0.0.1 - - [03/Jun/2026 15:30:45] "POST /webhook/line HTTP/1.1" 200 -
127.0.0.1 - - [03/Jun/2026 15:30:46] "POST /webhook/line HTTP/1.1" 200 -
```

這表示伺服器成功接收和處理了 LINE 的請求。

### 4.2 常見問題排除

#### 問題 1：Bot 沒有回應

**可能原因**：
- Webhook URL 未設定或不正確
- LINE 無法訪問你的伺服器

**解決方案**：
- 確認 ngrok 仍在運行
- 確認 Webhook URL 是 HTTPS（不是 HTTP）
- 在 LINE Developers 後台測試 Webhook 連接（應該會看到 200 status）

#### 問題 2：收到錯誤訊息

**可能原因**：
- .env 檔案配置有誤
- LINE Token 過期

**解決方案**：
- 檢查 .env 中的 LINE_CHANNEL_SECRET 和 LINE_CHANNEL_ACCESS_TOKEN
- 如果 Token 過期，在 LINE Developers 後台重新生成

#### 問題 3：距離計算不準確

**可能原因**：
- 座標設定有誤

**解決方案**：
- 驗證 .env 中的 COMPANY_LATITUDE 和 COMPANY_LONGITUDE
- 使用 Google Maps 驗證座標是否正確

---

## ✅ 完整測試檢查清單

```
伺服器啟動
□ Flask 伺服器已啟動（http://0.0.0.0:5000）
□ 健康檢查 API 正常（curl http://localhost:5000/health）
□ ngrok 已啟動並轉發正確的 URL

LINE 配置
□ Webhook URL 已在 LINE Developers 後台設定
□ Webhook 連接已驗證（200 status）
□ Bot 已加入 LINE

基本功能
□ 傳送「午餐」有回應
□ 收到篩選選單卡片
□ 點擊按鈕有反應

篩選功能
□ 300m 篩選正常（距離 < 300m）
□ 600m 篩選正常（距離 < 600m）
□ 1km 篩選正常（距離 < 1000m）
□ 1.5km 篩選正常（距離 < 1500m）

隨機性
□ 多次抽籤有不同結果
□ 不是每次都抽到同一間餐廳

導航
□ Google Maps 按鈕可點擊
□ 打開 Google Maps 顯示正確位置

整體評分
□ 功能完整
□ 使用者體驗良好
□ 沒有明顯的 Bug
```

---

## 📊 測試報告範本

**測試日期**：2026-06-03  
**測試人員**：你的名字  
**測試環境**：本地開發伺服器

| 測試項目 | 預期結果 | 實際結果 | 狀態 | 備註 |
|---------|---------|---------|------|------|
| 伺服器啟動 | 成功 | | ✅/❌ | |
| 健康檢查 | 200 | | ✅/❌ | |
| 基本對話 | 收到選單卡片 | | ✅/❌ | |
| 300m 篩選 | 距離 < 300m | | ✅/❌ | |
| 600m 篩選 | 距離 < 600m | | ✅/❌ | |
| 1km 篩選 | 距離 < 1000m | | ✅/❌ | |
| 1.5km 篩選 | 距離 < 1500m | | ✅/❌ | |
| 隨機性 | 有不同結果 | | ✅/❌ | |
| Google Maps | 可點擊 | | ✅/❌ | |

---

## 🎯 測試完成後

### 收集結果

測試完成後，告訴我：

```
✅ 哪些功能正常
❌ 哪些功能有問題（如有）
💭 使用者體驗感受
```

### 我會

- ✅ 修復任何 Bug
- ✅ 優化使用者體驗
- ✅ 添加新功能（如需要）
- ✅ 準備部署到 Render

---

## 💡 測試技巧

### 1. 保持終端可見

在測試時，保持 Flask 伺服器的終端窗口開著，這樣你能看到實時日誌。

### 2. 使用 LINE 的開發者工具

在 LINE Developers 後台，有個「Webhook 測試」功能，可以模擬發送訊息。

### 3. 逐步測試

不要一次測試所有功能。逐個驗證，這樣容易找到問題。

### 4. 記錄結果

記下哪些正常、哪些有問題，方便後續修復。

---

## 🆘 需要幫助？

**如果測試遇到問題**：

1. 檢查終端的錯誤訊息
2. 查看伺服器日誌
3. 驗證 .env 配置
4. 告訴我遇到的問題，我會幫你除錯

**常用除錯命令**：

```bash
# 測試健康檢查
curl http://localhost:5000/health

# 測試 Webhook（模擬 LINE 訊息）
curl -X POST http://localhost:5000/webhook/line \
  -H "Content-Type: application/json" \
  -H "X-Line-Signature: test" \
  -d '{"events":[{"type":"message","message":{"type":"text","text":"午餐"}}]}'

# 查看資料庫中的餐廳
python -c "from src.database.queries import get_all_restaurants; restaurants = get_all_restaurants(); print(f'Total: {len(restaurants)}'); [print(f'  {r.name}: {r.distance}') for r in restaurants]"
```

---

**準備好測試了嗎？** 🚀

按照上面的步驟進行，有任何問題隨時告訴我！

Last Updated: 2026-06-03
