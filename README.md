# Link Conversion - 連結轉換工具

一個簡單易用的連結轉換工具，可去除社交平台連結中的追蹤參數。

## 功能特點

- ✅ **完全免費** - 無需任何維護成本
- ✅ **離線使用** - 下載後可直接使用，無需網路連線
- ✅ **跨平台兼容** - 支援手機、平板電腦和電腦
- ✅ **簡單介面** - 直觀易用，無需學習成本
- ✅ **隱私保護** - 去除追蹤參數，防止被追蹤

## 支援的平台

- Facebook
- Instagram
- YouTube
- X (Twitter)
- Threads

## Bot 整合（簡便部署）

現在我們提供了三個平台的完整 Bot 實現，您可以直接部署使用：

### 🤖 Telegram Bot
- 自動偵測和轉換連結
- 簡單的配置流程
- [查看配置說明](bots/README.md#1️⃣-telegram-bot)

### 🎮 Discord Bot  
- 自動轉換 + 手動命令
- 美觀的 Embed 輸出
- [查看配置說明](bots/README.md#2️⃣-discord-bot)

### 📱 WhatsApp Bot
- 基於官方 Cloud API
- Webhook 自動回覆
- [查看配置說明](bots/README.md#3️⃣-whatsapp-bot)

所有 Bot 代碼都在 [`bots/`](bots/) 目錄中，包含完整的配置說明。

## 使用方法

### 方法一：直接在瀏覽器開啟

1. 將 `index.html` 文件下載到您的裝置
2. 使用任何瀏覽器（Chrome、Safari、Firefox 等）開啟檔案
3. 輸入或貼上需要轉換的連結
4. 點擊「轉換連結」按鈕
5. 複製轉換後的乾淨連結

### 方法二：部署為 Web 應用

您可以將此應用程式部署到任何靜態網頁託管服務：

- **GitHub Pages**
  ```bash
  # 將檔案推送到 GitHub 倉庫
  git push origin main
  # 在倉庫設定中啟用 GitHub Pages
  ```

- **Netlify**
  - 直接拖放 `index.html` 到 Netlify Drop

- **Vercel**
  - 連接 GitHub 倉庫自動部署

### 方法三：整合到 Bot

我們已經提供了完整的 Bot 實現，位於 [`bots/`](bots/) 目錄：

- **Telegram Bot**: `bots/telegram_bot.py` - 自動偵測和轉換連結
- **Discord Bot**: `bots/discord_bot.py` - 支援自動轉換和手動命令
- **WhatsApp Bot**: `bots/whatsapp_bot.py` - 基於官方 Cloud API

詳細配置說明請查看 [`bots/README.md`](bots/README.md)。

## 轉換範例

| 原始連結 | 轉換後連結 |
|---------|-----------|
| `https://www.instagram.com/p/DZQ_TWrlCRS/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ==` | `https://www.instagram.com/p/DZQ_TWrlCRS` |
| `https://youtu.be/iRSu_af96q8?si=UpTOo8--4Ca-h8P6` | `https://www.youtube.com/watch?v=iRSu_af96q8` |
| `https://x.com/user/status/123456?s=20` | `https://x.com/user/status/123456` |

## 技術架構

- **純 HTML/CSS/JavaScript** - 無需任何框架或依賴
- **單檔案設計** - 所有功能集中在一個 HTML 檔案中
- **響應式設計** - 自動適應各種螢幕尺寸

## 授權

MIT License - 自由使用、修改和分發