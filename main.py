# main.py
import os
from telegram.ext import ApplicationBuilder
from handlers import start_handler, message_handler

def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN_TEMP")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(start_handler)
    app.add_handler(message_handler)

    print("🟢 PrimoGPT attivo su Render...")
    app.run_polling()

if __name__ == "__main__":
    main()
