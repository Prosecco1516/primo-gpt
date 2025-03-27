# main.py
import os
import asyncio
from telegram.ext import ApplicationBuilder
from handlers import start_handler, message_handler


async def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Es: https://tuo-bot.onrender.com/webhook

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(start_handler)
    app.add_handler(message_handler)

    print("🟢 PrimoGPT attivo in modalità webhook...")

    await app.run_polling()

    )


if __name__ == "__main__":
    import nest_asyncio
    import asyncio

    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())

