from telegram.ext import ApplicationBuilder
from bot.handlers import start_handler, message_handler

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

import os
application = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()

application.add_handler(start_handler)
application.add_handler(message_handler)

print("🟢 PrimoGPT attivo su Render...")
application.run_polling()
