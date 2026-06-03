# 🔗 GitHub 設定指南

本指南將帶你逐步將 AutoLunch 專案推送到 GitHub。

---

## 📋 前置準備（5 分鐘）

### 1️⃣ 確保你有 GitHub 帳戶

- 如無：前往 [GitHub.com](https://github.com) 申請免費帳戶
- 如有：確保已登入

### 2️⃣ 安裝 Git

**Windows**：
```bash
# 檢查是否已安裝
git --version

# 如未安裝，下載並安裝：
# https://git-scm.com/download/win
```

**macOS/Linux**：
```bash
git --version
```

### 3️⃣ 設定 Git 使用者信息

```bash
git config --global user.name "你的名字"
git config --global user.email "你的 Email（需與 GitHub 帳戶相同）"

# 驗證設定
git config --global user.name
git config --global user.email
```

---

## 🚀 連接 GitHub（3 種方式）

### 方式 A：使用 HTTPS（推薦新手）

**步驟 1**：在 GitHub 上建立新倉庫

1. 登入 [GitHub](https://github.com)
2. 點擊右上角 `+` → `New repository`
3. 填入以下信息：
   ```
   Repository name: autolunch
   Description: LINE 午餐抽籤機器人
   Visibility: Public（開源）或 Private（私人）
   Initialize: 不勾選（本地已有檔案）
   ```
4. 點擊 `Create repository`

**步驟 2**：複製倉庫 URL

在新建的倉庫頁面，找到綠色的 `Code` 按鈕：
```
選擇 HTTPS 標籤，複製 URL
格式：https://github.com/你的用户名/autolunch.git
```

**步驟 3**：在本地初始化並推送

```bash
cd c:\Users\Enchung_Chang\Desktop\AutoLunch

# 初始化 git 倉庫
git init

# 添加所有檔案
git add .

# 建立首次提交
git commit -m "Initial commit: AutoLunch LINE Bot 系統架構"

# 連接到遠端倉庫（把 URL 替換為你複製的）
git remote add origin https://github.com/你的用户名/autolunch.git

# 重命名分支為 main（若需要）
git branch -M main

# 推送到 GitHub
git push -u origin main
```

✅ 完成！訪問 GitHub 倉庫確認檔案已上傳。

---

### 方式 B：使用 SSH（推薦進階用户）

**優點**：無需每次都輸入密碼

**步驟 1**：生成 SSH 金鑰

```bash
# 生成新的 SSH 金鑰
ssh-keygen -t ed25519 -C "你的 GitHub Email"

# 按 Enter 三次（使用預設路徑和空密碼）
```

**步驟 2**：添加公鑰到 GitHub

```bash
# 複製公鑰
# Windows PowerShell:
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard

# macOS/Linux:
cat ~/.ssh/id_ed25519.pub | pbcopy
```

1. 登入 GitHub → Settings → SSH and GPG keys
2. 點擊 `New SSH key`
3. 粘貼公鑰，點擊 `Add SSH key`

**步驟 3**：測試連接

```bash
ssh -T git@github.com
# 預期輸出：Hi [username]! You've successfully authenticated...
```

**步驟 4**：推送到 GitHub

```bash
cd c:\Users\Enchung_Chang\Desktop\AutoLunch

git init
git add .
git commit -m "Initial commit: AutoLunch LINE Bot 系統架構"

# 使用 SSH 地址（從 GitHub Code 按鈕的 SSH 標籤複製）
git remote add origin git@github.com:你的用户名/autolunch.git

git branch -M main
git push -u origin main
```

---

### 方式 C：使用 GitHub CLI（最簡單）

**安裝 GitHub CLI**：

```bash
# Windows (使用 Winget 或 Chocolatey)
winget install --id GitHub.cli

# 或下載：https://cli.github.com
```

**初始化並推送**：

```bash
cd c:\Users\Enchung_Chang\Desktop\AutoLunch

# 登入 GitHub
gh auth login
# 按提示選擇 HTTPS，完成驗證

# 初始化 git
git init
git add .
git commit -m "Initial commit: AutoLunch LINE Bot 系統架構"

# 使用 GitHub CLI 建立倉庫並推送
gh repo create autolunch --source=. --remote=origin --push
```

✨ **完全自動化！** 倉庫已建立並推送完成。

---

## 🔄 日常 Git 操作

### 保存你的工作

```bash
# 1. 查看修改的檔案
git status

# 2. 添加修改
git add .

# 3. 提交
git commit -m "簡短的修改說明"

# 4. 推送到 GitHub
git push
```

### 建議的提交訊息格式

```
feat: 新增距離篩選功能
fix: 修復座標計算錯誤
docs: 更新 README 文檔
refactor: 重構地理計算服務
test: 添加單元測試
```

### 檢查推送狀態

```bash
# 查看本地分支與遠端的差異
git log --oneline -5

# 查看遠端狀態
git remote -v
```

---

## 🚨 常見問題排除

### 問題 1：`fatal: not a git repository`

```bash
# 解決：在專案目錄初始化 git
cd c:\Users\Enchung_Chang\Desktop\AutoLunch
git init
```

### 問題 2：`Permission denied (publickey)`（SSH 問題）

```bash
# 檢查 SSH 連接
ssh -T git@github.com

# 如失敗，改用 HTTPS：
git remote set-url origin https://github.com/你的用户名/autolunch.git
```

### 問題 3：`fatal: 'origin' does not appear to be a 'git' repository`

```bash
# 檢查遠端設定
git remote -v

# 重新添加遠端
git remote remove origin
git remote add origin https://github.com/你的用户名/autolunch.git
```

### 問題 4：推送被拒絕

```bash
# 如遠端倉庫有初始提交（如 README），先拉取
git pull origin main --allow-unrelated-histories

# 再推送
git push -u origin main
```

---

## 📊 推薦的 .gitignore（已準備）

檔案 [.gitignore](./.gitignore) 已包含：
- Python 虛擬環境 (`venv/`)
- IDE 設定 (`.vscode/`, `.idea/`)
- 環境變數 (`.env`, `.env.local`)
- 資料庫檔案 (`*.db`)
- 日誌檔案 (`logs/`, `*.log`)

✅ 已自動配置，無需修改。

---

## ✅ 完整推送檢查清單

```
□ GitHub 帳戶已建立
□ Git 已安裝且配置
□ 本地 git 倉庫已初始化
□ 檔案已添加到 staging
□ 首次提交已建立
□ 遠端倉庫已連接
□ 檔案已推送到 GitHub

全部完成？→ 專案上線 GitHub ✅
```

---

## 🔍 驗證推送是否成功

### 方式 1：在瀏覽器檢查

1. 打開你的 GitHub 倉庫 URL：
   ```
   https://github.com/你的用户名/autolunch
   ```
2. 檢查檔案是否都已上傳
3. 查看 `README.md` 是否能正確顯示

### 方式 2：在終端檢查

```bash
# 查看遠端倉庫信息
git remote -v

# 查看推送歷史
git log --oneline

# 檢查當前分支
git branch -a
```

---

## 📚 GitHub Workflow（部署後）

建議的開發工作流：

```
功能開發分支
├─ git checkout -b feature/distance-filter
├─ 編寫代碼 & 提交
└─ git push origin feature/distance-filter
     ↓
提交 Pull Request (GitHub)
     ↓
代碼審查 & 測試
     ↓
合併到 main 分支
     ↓
自動部署到 Render（後續設定）
```

---

## 🎯 推薦方案

對於你的情況，**推薦使用「方式 A：HTTPS」**：

✅ **優點**：
- 設定簡單，只需複製粘貼
- 無需生成金鑰
- 適合個人項目

⚠️ **缺點**：
- 每次推送可能需要輸入密碼（GitHub 已自動記憶）

---

## 🚀 立即開始

### 快速 3 步推送

```bash
# 1. 進入專案目錄
cd c:\Users\Enchung_Chang\Desktop\AutoLunch

# 2. 初始化並推送（複製下方整塊代碼執行）
git init
git add .
git commit -m "Initial commit: AutoLunch LINE Bot 系統架構"
git remote add origin https://github.com/你的用户名/autolunch.git
git branch -M main
git push -u origin main

# 3. 完成！訪問 https://github.com/你的用户名/autolunch 確認
```

---

## 📞 需要幫助？

- **忘記 GitHub 用户名？**：登入 GitHub → Settings → Profile
- **需要建立新倉庫？**：GitHub 首頁 → `+` → `New repository`
- **SSH 金鑰問題？**：參考 [GitHub SSH 官方文檔](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

**準備好了？按上方「快速 3 步推送」開始吧！** 🚀

Last Updated: 2026-06-03
