# main.py
import os
import asyncio
from telegram.ext import ApplicationBuilder
from bot.handlers import start_handler, message_handler


async def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Es: https://tuo-bot.onrender.com/webhook

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(start_handler)
    app.add_handler(message_handler)

    print("🟢 PrimoGPT attivo in modalità webhook...")

    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=WEBHOOK_URL,
    )


if __name__ == "__main__":
    asyncio.run(main())
