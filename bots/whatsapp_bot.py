#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WhatsApp Bot - 連結轉換工具
使用 WhatsApp Cloud API 自動將用戶發送的社交平台連結轉換為乾淨連結
"""

import os
import re
import requests
from flask import Flask, request, jsonify
from urllib.parse import urlparse, parse_qs, urlencode

app = Flask(__name__)

# ============= 配置 =============
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
VERIFY_TOKEN = os.getenv('WHATSAPP_VERIFY_TOKEN', 'my_verify_token')

# WhatsApp API 端點
WHATSAPP_API_URL = "https://graph.facebook.com/v17.0"


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


def process_links(text: str) -> list:
    """處理文本中的所有連結"""
    links = extract_links(text)
    
    if not links:
        return []
    
    results = []
    for link in links:
        converted = convert_link(link)
        results.append({
            'original': link,
            'clean': converted
        })
    
    return results


# ============= WhatsApp API 函數 =============
def send_whatsapp_message(to_number: str, message: str):
    """發送 WhatsApp 消息"""
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    
    response = requests.post(
        f"{WHATSAPP_API_URL}/{WHATSAPP_PHONE_NUMBER_ID}/messages",
        headers=headers,
        json=data
    )
    
    return response.json()


def handle_user_message(from_number: str, message_text: str):
    """處理用戶消息"""
    results = process_links(message_text)
    
    if results:
        # 構建回應消息
        response_lines = ["🔗 連結轉換結果：\n"]
        
        for i, result in enumerate(results[:5], 1):  # 最多顯示 5 個連結
            response_lines.append(f"{i}. 原始：{result['original']}")
            response_lines.append(f"   乾淨：{result['clean']}")
            response_lines.append("")
        
        if len(results) > 5:
            response_lines.append(f"...還有 {len(results) - 5} 個連結")
        
        response_message = "\n".join(response_lines)
        send_whatsapp_message(from_number, response_message)
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
        send_whatsapp_message(from_number, help_text)


# ============= Flask Webhook 路由 =============
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """驗證 Webhook（Facebook 需要）"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("✅ Webhook 驗證成功")
        return challenge, 200
    else:
        print("❌ Webhook 驗證失敗")
        return 'Verification failed', 403


@app.route('/webhook', methods=['POST'])
def receive_webhook():
    """接收 WhatsApp 消息"""
    data = request.get_json()
    
    # 檢查是否是 WhatsApp 消息
    if data.get('object') != 'whatsapp_business_account':
        return 'Invalid object', 400
    
    # 處理消息
    try:
        entry = data['entry'][0]
        changes = entry.get('changes', [])
        
        for change in changes:
            value = change.get('value', {})
            messages = value.get('messages', [])
            
            for message in messages:
                if message.get('type') == 'text':
                    from_number = message['from']
                    message_text = message['text']['body']
                    
                    print(f"收到來自 {from_number} 的消息：{message_text}")
                    
                    # 處理消息（在背景線程中發送回應，避免超時）
                    handle_user_message(from_number, message_text)
        
        return 'EVENT_RECEIVED', 200
    
    except Exception as e:
        print(f"處理消息時出錯：{e}")
        return 'ERROR', 500


@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({'status': 'healthy'}), 200


# ============= 主程式 =============
def main():
    """主程式入口"""
    # 檢查必要的環境變數
    if not WHATSAPP_TOKEN:
        print("錯誤：請設置環境變數 WHATSAPP_TOKEN")
        print("可以通過以下方式設置：")
        print("export WHATSAPP_TOKEN='your_token_here'")
        return
    
    if not WHATSAPP_PHONE_NUMBER_ID:
        print("錯誤：請設置環境變數 WHATSAPP_PHONE_NUMBER_ID")
        print("可以通過以下方式設置：")
        print("export WHATSAPP_PHONE_NUMBER_ID='your_phone_number_id_here'")
        return
    
    print("🤖 WhatsApp Bot 正在啟動...")
    print(f"Webhook 端點：/webhook")
    print(f"健康檢查端點：/health")
    print("\n請在 Facebook Developer Console 中配置 Webhook URL:")
    print("https://your-domain.com/webhook")
    print(f"Verify Token: {VERIFY_TOKEN}")
    
    # 啟動 Flask 應用
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)


if __name__ == '__main__':
    main()
