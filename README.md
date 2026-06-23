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

由於這是純 HTML/JavaScript 實現，您可以輕鬆整合到：
- Telegram Bot
- Discord Bot
- WhatsApp Bot

只需提取 `convertLink()` 函數並整合到您的 Bot 程式碼中即可。

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