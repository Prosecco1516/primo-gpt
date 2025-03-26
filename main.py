# main.py
import os
from telegram.ext import ApplicationBuilder
from bot.handlers import start_command, handle_message

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL") + WEBHOOK_PATH

application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

application.add_handler(start_command)
application.add_handler(handle_message)

print("🟢 Avvio webhook...")

application.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get("PORT", 10000)),
    webhook_url=WEBHOOK_URL
)
