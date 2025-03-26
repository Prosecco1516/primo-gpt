from telegram.ext import ApplicationBuilder
from bot.handlers import start_command, handle_message
import os

if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    application.add_handler(start_command)
    application.add_handler(handle_message)

    print("🟢 PrimoGPT avviato...")
    application.run_polling()  # Niente asyncio qui!
