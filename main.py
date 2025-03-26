import os
import asyncio
from telegram.ext import ApplicationBuilder
from bot.handlers import start_command, handle_message_handler

async def main():
    telegram_token = os.getenv("TELEGRAM_TOKEN")

    if not telegram_token:
        print("❌ TELEGRAM_TOKEN non impostato.")
        return

    application = ApplicationBuilder().token(telegram_token).build()
    application.add_handler(start_command)
    application.add_handler(handle_message_handler)

    print("🟢 PrimoGPT avviato...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
