import requests
from io import BytesIO
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Use your bot token here
TELEGRAM_BOT_TOKEN = "7893760805:AAGoUUIEKZYHJyuGg5Kojop1LtESjpgu-50"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to HaldarAi 💡\nHaldarAi 💡 is an AI-powered tool to help you create unique images from text prompts. All your creations are saved locally on your device for privacy."
    )

async def handle_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text.strip()
    if not prompt:
        await update.message.reply_text("⚠️ Please send a non-empty prompt.")
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO
    )

    try:
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?nologo=true"
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()

        bio = BytesIO(resp.content)
        bio.name = "pollinations.jpg"
        bio.seek(0)

        await update.message.reply_photo(photo=bio, caption=f"Prompt: {prompt[:100]}")
    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("😕 Error generating image, please try again later.")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prompt))

    print("✅ HaldarAi 💡 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
