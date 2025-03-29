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

# Flag per mostrare il messaggio introduttivo solo una volta per utente
shown_intro = set()

# Modalità di apprendimento attiva (attivabile con "Primo ti insegno")
learning_mode = set()

# Inferenzia il topic sulla base del messaggio
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
    elif "ruota" in msg or "bucata" in msg or "panne" in msg or "fermo" in msg:
        return "disguido"
    return "altro"

# Salva su Google Sheet
def save_to_sheet(user, message, response, topic, contesto="generale", fase="auto"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user, message, response, topic, contesto, fase])

# Gestione messaggi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.full_name
    message = update.message.text
    chat_type = update.message.chat.type

    topic = inferisci_topic(message)

    # Modalità apprendimento attiva?
    if message.lower().startswith("primo ti insegno"):
        learning_mode.add(user)
        intro = "📝 Ok, ho trascritto l'istruzione.\n👂 Sto aggiornando il mio cervello. Quando sentirò 'appuntamento', inizierò a ragionare sul servizio richiesto e guiderò il cliente passo dopo passo.\n⚙️ Non clicco ancora sul gestionale, ma imparo il modo giusto di farlo.\n💬 Ora se vuoi aiutarmi davvero, scrivimi un esempio così:\nCliente: ...\nPrimo: ..."
        await update.message.reply_text(intro)
        save_to_sheet(user, message, intro, topic, "apprendimento", "istruzione")
        return

    # Apprendimento con esempio
    if user in learning_mode and "cliente:" in message.lower() and "primo:" in message.lower():
        response = "✅ Ricevuto! Vuoi aggiungere un altro esempio per entrare ancora più nel dettaglio o passiamo alla validazione?"
        await update.message.reply_text(response)
        save_to_sheet(user, message, response, topic, "apprendimento", "esempio")
        return

    # Logica classica
    if "appuntamento" in message.lower():
        response = "📅 Vuoi fissare un appuntamento. Ti serve fissarne uno nuovo o spostarne uno? E puoi lasciare la macchina o aspetti in sede?"
    elif message.lower().strip() == "revisione":
        response = "🚗 Ti consiglio la sede di Via San Donà. Vuoi che ti metta in contatto?\n\n📞 Finché non mi allenate a fare bene il mio lavoro, i ragazzi della meccanica faticano a rispondere a tutte le chiamate!"
    elif message.lower().strip() == "pneumatici":
        response = "🛞 Ti consiglio la sede del Centro La Piazza. Vuoi che ti fissi l’appuntamento?"
    elif message.lower().strip() == "meccanica":
        response = "🔧 Sembra che tu voglia fare le cose fatte bene. I nostri meccanici sono i migliori, ma servono info precise. Vuoi procedere?"
    elif topic == "disguido":
        response = "🔧 Sembra un problema urgente. Vuoi che ti metta in contatto subito con l'officina più vicina o che ti dia dei consigli utili per gestire la situazione?"
    else:
        response = "🤖 Ciao! Sto alla grande perché sto imparando.\n\nIn questo periodo mi sto concentrando su come gestire gli appuntamenti nel modo migliore. Ogni conversazione che assomiglia a una telefonata con un cliente mi aiuta tantissimo.\n\nSe vuoi aiutarmi davvero, spiegami bene il contesto:\n• scrivi 'Cliente: ...'\n• scrivi subito dopo 'Primo: ...'\n\nOppure se vuoi insegnarmi qualcosa di nuovo, inizia con 'Primo ti insegno ...'"
        save_to_sheet(user, message, response, topic, "orientamento", "intro")
        await update.message.reply_text(response)
        return

    await update.message.reply_text(response)

    # Salva risposta se c'è la parola 'istruzione'
    if "istruzione" in message.lower():
        save_to_sheet(user, message, response, topic, "apprendimento", "istruzione")

    # Disabilita temporaneamente il gruppo per non sporcarlo
    if chat_type != "private":
        return
