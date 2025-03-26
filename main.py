import logging
import openai
import os
import os.path
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, Bot
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Setup logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# Telegram bot token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Google Sheets setup con controllo robusto
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

SHEET_ENABLED = False
if os.path.exists("credentials.json"):
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key("109018550274954569288").sheet1
        SHEET_ENABLED = True
        print("✅ Google Sheets attivo")
    except Exception as e:
        print(f"⚠️ Errore nell'accesso a Google Sheets: {e}")
else:
    print("⚠️ File credentials.json non trovato. Sheets disattivato.")

# Funzione per determinare la sede

def determina_sede(messaggio):
    messaggio = messaggio.lower()
    if any(x in messaggio for x in ["pneumatic", "gomme", "stagionali", "convergenza"]):
        return "Pneumatici"
    elif any(x in messaggio for x in ["meccanica", "revisione", "tagliando", "freni", "motore"]):
        return "Meccanica e Revisioni"
    elif any(x in messaggio for x in ["lucidatura", "coating", "ppf", "lavaggio", "interni"]):
        return "Detailing"
    else:
        return "Non specificato"

# Start command
def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text("Ciao! Sono Primo 🤖. Come posso aiutarti oggi?")

# Messaggi testuali
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    if "appuntamento" in user_message.lower():
        sede = determina_sede(user_message)
        if sede != "Non specificato":
            reply_text = (
                f"Perfetto! Da quanto mi hai scritto, il servizio riguarda la sede *{sede}*\n"
                "Posso chiederti:\n- Nome\n- Cognome\n- Cellulare\n- Tipo di servizio esatto?\n\n"
                "Così ti aiuto a fissare l'appuntamento giusto 🚀"
            )
        else:
            reply_text = (
                "Perfetto! Ti aiuto a fissare l’appuntamento. Prima dimmi:\n"
                "- Che tipo di servizio ti serve? (es. gomme, meccanica, lucidatura...)\n"
                "In base a quello ti indirizzo nella sede corretta."
            )

        await update.message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)
        return

    if "come stai" in user_message.lower():
        await update.message.reply_text("Sto alla grande, grazie che me lo chiedi! Se hai bisogno di aiuto per un appuntamento o un dubbio tecnico, sono qui ✌️")
        return

    await update.message.reply_text("Ricevuto! Dimmi pure cosa posso fare per te ✨")

# Main bot setup
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
