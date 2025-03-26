# main.py
import logging
import openai
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.handlers import start_command, handle_message
from bot.sheet import setup_google_sheet
from bot.delete_webhook import delete_webhook_if_exists

# Setup logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# Telegram bot token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Setup Google Sheet
SHEET_ENABLED, sheet = setup_google_sheet()

# Funzione per salvare istruzioni e risposte
async def salva_istruzione(sheet, utente, messaggio, risposta):
    try:
        sheet.append_row([utente, messaggio, risposta])
        print("✅ Istruzione salvata su Google Sheet")
    except Exception as e:
        print(f"⚠️ Errore nel salvataggio su Google Sheet: {e}")

# Avvio bot
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).post_init(delete_webhook_if_exists).build()

    application.bot_data["SHEET_ENABLED"] = SHEET_ENABLED
    application.bot_data["sheet"] = sheet
    application.bot_data["salva_istruzione"] = salva_istruzione

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ PrimoGPT avviato. In ascolto su Telegram...")
    application.run_polling()

if __name__ == "__main__":
    main()
