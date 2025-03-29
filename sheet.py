# sheet.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
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


def save_to_sheet(user, message, response, topic):
    timestamp = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user, message, response, topic])


# Handler da integrare in handlers.py
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.full_name
    message = update.message.text
    chat_type = update.message.chat.type

    # Carattere di Primo mostrato una sola volta per utente
    tono_intro = "🤖 Primo | Sono l'ultimo arrivato, sto imparando! Ora il mio obiettivo è diventare bravissimo a gestire appuntamenti, telefonate e aiutare in ogni situazione. Dimmi come posso esserti utile."

    # Analisi topic prima della risposta
    topic = inferisci_topic(message)

    # Logica intelligente di risposta
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
        response = "💡 Per aiutarmi ad allenarmi, scrivi una frase con la parola 'istruzione'. Oppure dimmi se hai bisogno di un aiuto su ferie, appuntamenti o se hai avuto un problema."

    # Salvataggio solo se contiene la parola 'istruzione'
       if "istruzione" in message.lower():
        save_to_sheet(user, message, response, topic)
        await update.message.reply_text(
            "📝 Ok, ho trascritto l’istruzione.\n"
            "👂 Sto aggiornando il mio cervello. Quando sentirò il contesto che mi hai raccontato, inizierò a ragionare su quella dinamica e guiderò il cliente passo passo.\n"
            "⚙️ Non clicco ancora sul gestionale, ma imparo il modo giusto di farlo.\n"
            "💬 Ora, se vuoi aiutarmi davvero, scrivimi un esempio concreto così:\n"
            "Cliente: ...\n"
            "Primo: ..."
        )


    # Mostra tono introduttivo solo se utente nuovo
    if user not in shown_intro:
        await update.message.reply_text(f"{tono_intro}\n\n{response}")
        shown_intro.add(user)
    else:
        await update.message.reply_text(response)

    # Disabilita temporaneamente il gruppo per non sporcarlo
    if chat_type != "private":
        return
