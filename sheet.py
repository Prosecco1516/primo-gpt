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

# Flag per utenti in modalità allenamento
training_mode = set()


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
    elif any(x in msg for x in ["ruota", "bucata", "panne", "fermo"]):
        return "disguido"
    elif any(x in msg for x in ["idea", "intuizione", "ho un'idea"]):
        return "idea"
    return "altro"


def save_to_sheet(user, message, response, topic, tipo="messaggio", fase="interazione"): 
    timestamp = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user, message, response, topic, tipo, fase])


# Handler da integrare in handlers.py
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.full_name
    message = update.message.text
    chat_type = update.message.chat.type

    # Mostra tono introduttivo solo se utente nuovo
    if user not in shown_intro:
        intro = (
            "🤖 Ciao! Sono Primo, l’ultimo arrivato. Mi sto allenando per aiutare con appuntamenti, clienti e problemi urgenti.\n\n"
            "🎯 Al momento mi sto concentrando sull’apprendere come gestire appuntamenti in modo perfetto, ma posso registrare qualsiasi istruzione utile all’azienda.\n\n"
            "✍️ Se vuoi insegnarmi qualcosa, inizia il messaggio con: 'Primo, ti insegno…'\n"
            "💡 Se vuoi contribuire con un’idea, scrivi: 'Primo, ho un’idea…'\n\n"
            "🧪 La modalità test è disattivata. Se vuoi aiutarmi a crescere, l’allenamento è la strada migliore."
        )
        await update.message.reply_text(intro)
        shown_intro.add(user)

    # Disabilita temporaneamente il gruppo per non sporcarlo
    if chat_type != "private":
        return

    topic = inferisci_topic(message)

    # Attivazione allenamento
    if any(x in message.lower() for x in ["primo ti insegno", "primo, ti insegno", "primo impara", "vuoi allenarti"]):
        training_mode.add(user)
        response = (
            "🧠 Ok, sono in modalità allenamento.\n"
            "📥 Sto registrando le istruzioni che riceverò.\n"
            "✅ Se saranno approvate, diventeranno parte delle mie risposte ufficiali.\n\n"
            "✍️ Ora, se vuoi aiutarmi davvero, scrivimi un esempio così:\n"
            "Cliente: cosa dice?\nPrimo: come dovrei rispondere?"
        )
        await update.message.reply_text(response)
        save_to_sheet(user, message, response, topic, tipo="istruzione", fase="attivazione allenamento")
        return

    # Fine allenamento
    if "fine allenamento" in message.lower():
        training_mode.discard(user)
        response = (
            "🛠️ Allenamento terminato.\n"
            "📬 Il team validerà le istruzioni ricevute.\n"
            "🧪 Quando saranno approvate, potranno essere testate.\n\n"
            "✍️ Se vuoi riprendere, scrivi: 'Primo, ti insegno…'"
        )
        await update.message.reply_text(response)
        return

    # Registrazione esempio se in allenamento
    if user in training_mode and message.lower().startswith("cliente:"):
        response = (
            "📚 Ricevuto! Questo mi aiuta a gestire meglio la conversazione.\n\n"
            "💡 Vuoi aggiungere un altro esempio?\n"
            "Oppure raccontarmi cosa faresti tu nel gestionale in questa fase?"
        )
        await update.message.reply_text(response)
        save_to_sheet(user, message, response, topic, tipo="esempio", fase="raccolta esempi")
        return

    if user in training_mode and any(x in message.lower() for x in ["gestionale", "clicco", "inserisco"]):
        response = (
            "⚙️ Ricevuto anche il flusso gestionale!\n\n"
            "📈 Se vuoi aggiungere altri dettagli, continua pure. Tutto verrà registrato per migliorarmi.\n"
            "📬 Quando il team validerà il tutto, sarò pronto a metterlo in pratica."
        )
        await update.message.reply_text(response)
        save_to_sheet(user, message, response, topic, tipo="processo gestionale", fase="dettaglio gestionale")
        return

    # Idee
    if "primo ho un'idea" in message.lower():
        response = (
            "💡 Idea registrata!\n"
            "Vuoi descrivermela meglio o aggiungere un contesto d’uso concreto?"
        )
        await update.message.reply_text(response)
        save_to_sheet(user, message, response, topic, tipo="idea", fase="iniziale")
        return

    # Default fallback
    response = "💡 Per allenarmi, scrivi una frase che inizi con 'Primo, ti insegno…' oppure 'Primo, ho un'idea…'"
    await update.message.reply_text(response)
    save_to_sheet(user, message, response, topic)
