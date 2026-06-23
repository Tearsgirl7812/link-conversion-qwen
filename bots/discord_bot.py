#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discord Bot - 連結轉換工具
自動將用戶發送的社交平台連結轉換為乾淨連結
"""

import os
import re
import discord
from discord.ext import commands
from urllib.parse import urlparse, parse_qs, urlencode

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


# ============= Bot 設定 =============
intents = discord.Intents.default()
intents.message_content = True  # 需要啟用此權限來讀取消息內容
bot = commands.Bot(command_prefix='!', intents=intents)


# ============= Bot 事件 =============
@bot.event
async def on_ready():
    """Bot 就緒事件"""
    print(f'✅ Discord Bot 已登入：{bot.user}')
    print(f'服務於 {len(bot.guilds)} 個伺服器')


@bot.event
async def on_message(message):
    """處理消息事件"""
    # 忽略 Bot 自己的消息
    if message.author == bot.user:
        return
    
    # 檢查消息是否包含連結
    user_message = message.content
    results = process_links(user_message)
    
    if results:
        # 構建回應嵌入
        embed = discord.Embed(
            title="🔗 連結轉換結果",
            color=discord.Color.blue()
        )
        
        for i, result in enumerate(results[:5], 1):  # 最多顯示 5 個連結
            embed.add_field(
                name=f"連結 {i}",
                value=f"**原始：**\n{result['original']}\n\n**乾淨：**\n{result['clean']}",
                inline=False
            )
        
        if len(results) > 5:
            embed.set_footer(text=f"還有 {len(results) - 5} 個連結未顯示")
        
        await message.channel.send(embed=embed)
    
    # 繼續處理其他命令
    await bot.process_commands(message)


@bot.command(name='convert')
async def convert_command(ctx, *, url: str = None):
    """手動轉換連結命令"""
    if not url:
        embed = discord.Embed(
            title="❌ 使用說明",
            description="請提供要轉換的連結\n\n用法：`!convert <連結>`",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    converted = convert_link(url)
    
    embed = discord.Embed(
        title="🔗 連結轉換結果",
        color=discord.Color.green()
    )
    embed.add_field(
        name="原始連結",
        value=url,
        inline=False
    )
    embed.add_field(
        name="乾淨連結",
        value=converted,
        inline=False
    )
    
    await ctx.send(embed=embed)


@bot.command(name='help')
async def help_command(ctx):
    """顯示幫助信息"""
    embed = discord.Embed(
        title="🤖 Link Conversion Bot 幫助",
        description="我可以幫您將社交平台的連結轉換為乾淨連結，去除追蹤參數。",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="✨ 自動轉換",
        value="直接發送包含連結的消息，我會自動為您轉換！",
        inline=False
    )
    
    embed.add_field(
        name="🔧 手動轉換",
        value="使用 `!convert <連結>` 命令手動轉換特定連結",
        inline=False
    )
    
    embed.add_field(
        name="📱 支援的平台",
        value="• Facebook\n• Instagram\n• YouTube\n• X (Twitter)\n• Threads",
        inline=False
    )
    
    embed.set_footer(text="🔒 完全保護您的隱私，不會儲存任何數據")
    
    await ctx.send(embed=embed)


# ============= 主程式 =============
def main():
    """主程式入口"""
    # 從環境變數獲取 Token
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        print("錯誤：請設置環境變數 DISCORD_BOT_TOKEN")
        print("可以通過以下方式設置：")
        print("export DISCORD_BOT_TOKEN='your_bot_token_here'")
        return
    
    print("🤖 Discord Bot 正在啟動...")
    
    # 啟動 Bot
    bot.run(token)


if __name__ == '__main__':
    main()
