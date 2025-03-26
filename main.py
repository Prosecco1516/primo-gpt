import os
from telegram.ext import ApplicationBuilder
from bot.handlers import start_handler, message_handler

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    application.add_handler(start_handler)
    application.add_handler(message_handler)

    print("🟢 PrimoGPT attivo su Render...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
