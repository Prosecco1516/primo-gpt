import os
from telegram.ext import ApplicationBuilder
from bot.handlers import start_handler, message_handler

application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
application.add_handler(start_handler)
application.add_handler(message_handler)

print("🟢 PrimoGPT avviato...")
application.run_polling()
