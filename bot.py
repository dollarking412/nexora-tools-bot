import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Get from Render environment variable

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Send me a TikTok link and I'll download it!\n\n"
        "Example: https://tiktok.com/@user/video/123456789"
    )

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    if "tiktok.com" not in url:
        return
    
    await update.message.reply_text("⏬ Downloading...")
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'video.mp4',
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
        
        with open('video.mp4', 'rb') as video:
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=video,
                caption=f"✅ Here's your TikTok!"
            )
        
        os.remove('video.mp4')
        
    except Exception as e:
        await update.message.reply_text("❌ Failed. Try another link!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))
    
    print("Bot is running...")
    app.run_olling()

if __name__ == "__main__":
    main()
