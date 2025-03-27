# main.py
import os
from telegram.ext import ApplicationBuilder
from handlers import start_handler, message_handler
import nest_asyncio
import asyncio

nest_asyncio.apply()

async def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    print("🟢 PrimoGPT attivo in modalità polling...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
