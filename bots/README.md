# Bots 配置說明

本目錄包含三個平台的 Bot 實現，可自動將用戶發送的社交平台連結轉換為乾淨連結。

## 📱 支援的平台

- **Telegram** - `telegram_bot.py`
- **Discord** - `discord_bot.py`
- **WhatsApp** - `whatsapp_bot.py`

---

## 🔧 通用依賴安裝

所有 Bot 都需要 Python 3.7+，請先安裝必要的依賴：

```bash
# 創建虛擬環境（推薦）
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安裝依賴
pip install python-telegram-bot discord.py flask requests
```

或者使用 requirements.txt：

```bash
pip install -r requirements.txt
```

---

## 1️⃣ Telegram Bot

### 獲取 Token

1. 在 Telegram 中搜尋 [@BotFather](https://t.me/BotFather)
2. 發送 `/newbot` 命令
3. 按照提示設置 Bot 名稱和用戶名
4. 獲取 API Token（格式類似：`123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）

### 配置方法

**方法一：環境變數（推薦）**

```bash
export TELEGRAM_BOT_TOKEN='your_bot_token_here'
```

**方法二：直接修改代碼**

在 `telegram_bot.py` 中找到：
```python
token = os.getenv('TELEGRAM_BOT_TOKEN')
```
改為：
```python
token = 'your_bot_token_here'
```

### 啟動 Bot

```bash
python telegram_bot.py
```

### 功能特點

- ✅ 自動偵測消息中的連結並轉換
- ✅ 支援 `/start` 命令顯示歡迎信息
- ✅ 支援多個連結同時轉換
- ✅ 友好的錯誤處理

---

## 2️⃣ Discord Bot

### 獲取 Token

1. 訪問 [Discord Developer Portal](https://discord.com/developers/applications)
2. 點擊 "New Application" 創建應用
3. 進入 "Bot" 頁面，點擊 "Add Bot"
4. 在 "Token" 區域點擊 "Copy" 獲取 Token
5. **重要**：啟用 "Message Content Intent"
   - 進入 "Bot" 頁面
   - 找到 "Privileged Gateway Intents"
   - 啟用 "MESSAGE CONTENT INTENT"
6. 邀請 Bot 到伺服器：
   - 進入 "OAuth2" → "URL Generator"
   - 選擇 scopes: `bot`
   - 選擇 permissions: `Send Messages`, `Embed Links`, `Read Message History`
   - 複製生成的 URL 並在瀏覽器開啟

### 配置方法

**方法一：環境變數（推薦）**

```bash
export DISCORD_BOT_TOKEN='your_bot_token_here'
```

**方法二：直接修改代碼**

在 `discord_bot.py` 中找到：
```python
token = os.getenv('DISCORD_BOT_TOKEN')
```
改為：
```python
token = 'your_bot_token_here'
```

### 啟動 Bot

```bash
python discord_bot.py
```

### 功能特點

- ✅ 自動偵測消息中的連結並轉換（最多 5 個）
- ✅ 使用 Embed 美化輸出
- ✅ 支援 `!convert <連結>` 手動轉換命令
- ✅ 支援 `!help` 顯示幫助信息
- ✅ 忽略 Bot 自己的消息，避免無限循環

---

## 3️⃣ WhatsApp Bot

### 獲取 Token 和 Phone Number ID

1. 訪問 [Meta for Developers](https://developers.facebook.com/)
2. 創建一個新應用或選擇現有應用
3. 添加 "WhatsApp" 產品
4. 在 "Getting Started" 頁面获取：
   - **Temporary Access Token**（測試用，有效期 24 小時）
   - **Phone Number ID**
   - **Sender ID**

### 永久 Token 配置（生產環境）

1. 進入 [Business Settings](https://business.facebook.com/settings)
2. 選擇您的 WhatsApp Business Account
3. 生成系統用戶 Token

### 配置 Webhook

1. 在 Meta Developer Console 的 WhatsApp 產品頁面
2. 進入 "Configuration" → "Webhooks"
3. 點擊 "Edit" 添加 Webhook URL：
   - **Callback URL**: `https://your-domain.com/webhook`
   - **Verify Token**: 自定義一個 token（預設：`my_verify_token`）
4. 訂閱消息事件：`messages`

### 配置方法

**環境變數配置：**

```bash
export WHATSAPP_TOKEN='your_access_token_here'
export WHATSAPP_PHONE_NUMBER_ID='your_phone_number_id_here'
export WHATSAPP_VERIFY_TOKEN='my_verify_token'
export PORT=5000
```

### 部署選項

**本地測試：**

```bash
python whatsapp_bot.py
```

**使用 ngrok 測試（推薦）：**

```bash
# 安裝 ngrok
# 訪問 https://ngrok.com/ 下載

# 啟動 ngrok
ngrok http 5000

# 將生成的 URL (如 https://xxx.ngrok.io) 配置為 Webhook URL
```

**部署到雲端平台：**

- **Heroku**: 創建 Procfile 並部署
- **Railway**: 直接連接 GitHub 倉庫
- **Render**: 部署為 Web Service
- **VPS**: 使用 systemd 或 supervisor 管理進程

### 功能特點

- ✅ 基於 WhatsApp Cloud API（官方正式版本）
- ✅ Webhook 自動接收消息
- ✅ 自動回覆轉換結果
- ✅ 健康檢查端點 `/health`
- ✅ 支援最多 5 個連結的同時轉換

---

## 🎯 使用範例

### Telegram / Discord

用戶發送：
```
看看這個影片：https://youtu.be/iRSu_af96q8?si=UpTOo8--4Ca-h8P6
還有這個：https://www.instagram.com/p/DZQ_TWrlCRS/?utm_source=ig_web_copy_link
```

Bot 回覆：
```
🔗 連結轉換結果：

1. 原始：https://youtu.be/iRSu_af96q8?si=UpTOo8--4Ca-h8P6
   乾淨：https://www.youtube.com/watch?v=iRSu_af96q8

2. 原始：https://www.instagram.com/p/DZQ_TWrlCRS/?utm_source=ig_web_copy_link
   乾淨：https://www.instagram.com/p/DZQ_TWrlCRS
```

### WhatsApp

用戶發送相同內容，會收到格式化的文字回覆。

---

## 🔒 安全建議

1. **不要將 Token 提交到 Git**
   - 使用 `.gitignore` 排除包含敏感信息的文件
   - 使用環境變數或配置文件（不提交到 Git）

2. **限制 Bot 權限**
   - Discord: 只授予必要的權限
   - Telegram: 設置群組權限
   - WhatsApp: 使用測試號碼開始

3. **速率限制**
   - 考慮添加消息頻率限制，防止濫用

---

## 🐛 常見問題

### Telegram Bot 無法接收消息
- 確認 Bot Token 正確
- 檢查是否已與 Bot 對話並發送 `/start`
- 確認網路連接正常

### Discord Bot 無法讀取消息
- 確認已啟用 "Message Content Intent"
- 確認 Bot 已在伺服器中且有發送消息權限
- 檢查 Bot 角色權限

### WhatsApp Webhook 驗證失敗
- 確認 Verify Token 匹配
- 確認 Webhook URL 可公開訪問
- 檢查防火牆設置

---

## 📄 授權

MIT License - 自由使用、修改和分發
