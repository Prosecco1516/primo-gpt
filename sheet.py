# sheet.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
from telegram import Update
from telegram.ext import ContextTypes
import asyncio

# Autenticazione con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Apri il foglio di lavoro tramite ID
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
sheet = client.open_by_key(SHEET_ID).sheet1

def inferisci_topic(message):
    msg = message.lower()
    if "appuntamento" in msg:
        return "appuntamento"
    elif "ferie" in msg:
        return "ferie"
    elif "errore" in msg:
        return "errore"
    elif "documento" in msg:
        return "documento"
    elif "preventivo" in msg:
        return "preventivo"
    elif "cliente" in msg:
        return "cliente"
    return "altro"

def save_to_sheet(user, message, response, topic):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user, message, response, topic])

# Handler da integrare in handlers.py
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.full_name
    message = update.message.text
    chat_type = update.message.chat.type

    # Carattere di Primo
    tono = "🤖 Primo | Sempre al tuo fianco per semplificarti la giornata."

    # Analisi topic prima della risposta
    topic = inferisci_topic(message)

    # Logica intelligente di risposta
    if "appuntamento" in message.lower():
        response = "📅 Vuoi fissare un appuntamento. Che tipo di servizio ti serve? (Revisione, Pneumatici, Meccanica?)"
    else:
        response = "💡 Per aiutarmi ad allenarmi, scrivi una frase con la parola 'istruzione'."

    # Gestione istruzioni
    if "istruzione" in message.lower():
        save_to_sheet(user, message, response, topic)
        await update.message.reply_text("📝 Ok, ho trascritto l'istruzione.")

    # Risposta finale con tono
    await update.message.reply_text(f"{tono}\n\n{response}")

    # Disabilita temporaneamente il gruppo per non sporcarlo
    if chat_type != "private":
        return
