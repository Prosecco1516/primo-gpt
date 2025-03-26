# main.py
import os
from telegram.ext import ApplicationBuilder
from bot.handlers import start_handler, message_handler

async def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DOMAIN = os.getenv("RENDER_EXTERNAL_URL")  # Render imposta questa var automaticamente

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(start_handler)
    app.add_handler(message_handler)

    print("🟢 PrimoGPT attivo su Render con webhook...")

    await app.initialize()
    await app.start()
    await app.bot.set_webhook(f"{DOMAIN}/webhook")
    await app.updater.start_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        url_path="/webhook",
        webhook_url=f"{DOMAIN}/webhook"
    )
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
