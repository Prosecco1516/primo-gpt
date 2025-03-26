from telegram.ext import ApplicationBuilder
from bot.handlers import start_command, handle_message
import os

if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    from bot.handlers import start_handler, message_handler

application.add_handler(start_handler)
application.add_handler(message_handler)


    print("🟢 PrimoGPT avviato...")
    application.run_polling()  # Niente asyncio qui!
