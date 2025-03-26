# main.py
import os
import asyncio
from telegram.ext import ApplicationBuilder
from bot.handlers import start_command, handle_message

async def main():
    # Legge il token da variabile ambiente
    telegram_token = os.getenv("TELEGRAM_TOKEN")

    if not telegram_token:
        print("❌ TELEGRAM_TOKEN non impostato.")
        return

    application = ApplicationBuilder().token(telegram_token).build()
    application.add_handler(start_command)
    application.add_handler(handle_message)

    print("🟢 PrimoGPT avviato...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
