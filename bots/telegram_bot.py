#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot - 連結轉換工具
自動將用戶發送的社交平台連結轉換為乾淨連結
"""

import os
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ============= 連結轉換核心函數 =============
def convert_link(url: str) -> str:
    """轉換單個連結，去除追蹤參數"""
    url = url.strip()
    
    if not url:
        return ''
    
    try:
        # 確保 URL 有協議
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        
        from urllib.parse import urlparse, parse_qs, urlencode
        
        parsed = urlparse(url)
        hostname = parsed.netloc.lower()
        
        # Facebook 轉換
        if 'facebook.com' in hostname or 'fb.com' in hostname:
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            return clean_url
        
        # Instagram 轉換
        if 'instagram.com' in hostname:
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            return clean_url
        
        # YouTube 轉換
        if 'youtube.com' in hostname or 'youtu.be' in hostname:
            if 'youtu.be' in hostname:
                # 短連結轉長連結
                video_id = parsed.path[1:]
                return f"https://www.youtube.com/watch?v={video_id}"
            else:
                # 長連結，提取 video ID
                params = parse_qs(parsed.query)
                video_id = params.get('v', [''])[0]
                if video_id:
                    return f"https://www.youtube.com/watch?v={video_id}"
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                return clean_url
        
        # X (Twitter) 轉換
        if 'x.com' in hostname or 'twitter.com' in hostname:
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            return clean_url
        
        # Threads 轉換
        if 'threads.net' in hostname:
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            return clean_url
        
        # 其他連結，移除常見追蹤參數
        common_tracking_params = ['utm_source', 'utm_medium', 'utm_campaign', 
                                  'utm_term', 'utm_content', 'si', 's', 'fbclid', 'igsh']
        params = parse_qs(parsed.query)
        clean_params = {k: v for k, v in params.items() if k not in common_tracking_params}
        
        query_string = urlencode(clean_params, doseq=True) if clean_params else ''
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if query_string:
            clean_url += f"?{query_string}"
        
        return clean_url
    
    except Exception as e:
        return f'無效的連結：{url}'


def extract_links(text: str) -> list:
    """從文本中提取所有連結"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    links = re.findall(url_pattern, text)
    return links


def process_links(text: str) -> str:
    """處理文本中的所有連結"""
    links = extract_links(text)
    
    if not links:
        return None
    
    results = []
    for link in links:
        converted = convert_link(link)
        results.append(f"原始：{link}\n乾淨：{converted}")
    
    return '\n\n'.join(results)


# ============= Bot 處理函數 =============
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理用戶消息"""
    user_message = update.message.text
    
    if not user_message:
        return
    
    # 檢查是否包含連結
    result = process_links(user_message)
    
    if result:
        response = f"🔗 連結轉換結果：\n\n{result}"
        await update.message.reply_text(response)
    else:
        # 如果沒有連結，回復使用說明
        help_text = (
            "🤖 請發送包含社交平台連結的消息，我會幫您轉換為乾淨連結！\n\n"
            "支援的平台：\n"
            "• Facebook\n"
            "• Instagram\n"
            "• YouTube\n"
            "• X (Twitter)\n"
            "• Threads\n\n"
            "例如：https://www.instagram.com/p/xxx/?utm_source=..."
        )
        await update.message.reply_text(help_text)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /start 命令"""
    welcome_text = (
        "👋 歡迎使用 Link Conversion Bot！\n\n"
        "我可以幫您將社交平台的連結轉換為乾淨連結，去除追蹤參數。\n\n"
        "✨ 使用方法：\n"
        "直接發送包含連結的消息給我即可。\n\n"
        "📱 支援的平台：\n"
        "• Facebook\n"
        "• Instagram\n"
        "• YouTube\n"
        "• X (Twitter)\n"
        "• Threads\n\n"
        "🔒 完全保護您的隱私，不會儲存任何數據。"
    )
    await update.message.reply_text(welcome_text)


# ============= 主程式 =============
def main():
    """主程式入口"""
    # 從環境變數獲取 Token
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("錯誤：請設置環境變數 TELEGRAM_BOT_TOKEN")
        print("可以通過以下方式設置：")
        print("export TELEGRAM_BOT_TOKEN='your_bot_token_here'")
        return
    
    print("🤖 Telegram Bot 正在啟動...")
    
    # 創建應用
    application = Application.builder().token(token).build()
    
    # 添加處理器
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.COMMAND & filters.Regex('^/start$'), start_command))
    
    # 啟動 Bot
    print("✅ Bot 已啟動，正在監聽消息...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
