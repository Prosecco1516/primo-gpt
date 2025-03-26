# main.py
import os
from telegram.ext import ApplicationBuilder
from bot.handlers import start_command, handle_message_handler

telegram_token = os.getenv("TELEGRAM_TOKEN")
if not telegram_token:
    print("❌ TELEGRAM_TOKEN non trovato.")
else:
    application = ApplicationBuilder().token(telegram_token).build()
    application.add_handler(start_command)
    application.add_handler(handle_message_handler)

    print("🟢 PrimoGPT avviato...")
    application.run_polling()
