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
user_mode = {}


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


def save_to_sheet(user, message, response, topic, tipo="generico"):
    timestamp = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user, message, response, topic, tipo])


# Handler da integrare in handlers.py
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.full_name
    message = update.message.text
    chat_type = update.message.chat.type

    # Analisi topic prima della risposta
    topic = inferisci_topic(message)

    # Controlla se l'utente ha attivato l'allenamento
    is_training = user_mode.get(user) == "training"

    # Attiva modalità allenamento
    if any(trigger in message.lower() for trigger in ["primo, ti insegno", "primo impara", "primo vuoi allenarti", "primo oggi impari"]):
        user_mode[user] = "training"
        response = (
            "🧠 Ok, sono in modalità allenamento.\n"
            "📥 Sto registrando le istruzioni che riceverò.\n"
            "✅ Se saranno approvate, diventeranno parte delle mie risposte ufficiali.\n\n"
            "✍️ Ora, se vuoi aiutarmi davvero, scrivimi un esempio così:\n"
            "Cliente: cosa dice?\n"
            "Primo: come dovrei rispondere?"
        )
        save_to_sheet(user, message, response, topic, tipo="attivazione")
        await update.message.reply_text(response)
        return

    # Registra istruzioni
    if is_training and ("cliente:" in message.lower() and "primo:" in message.lower()):
        response = (
            "📚 Ricevuto! Questo mi aiuta a migliorare la mia risposta.\n"
            "💬 Vuoi aggiungere un altro esempio?\n"
            "Oppure raccontarmi cosa faresti tu nel gestionale in questa fase?"
        )
        save_to_sheet(user, message, response, topic, tipo="esempio")
        await update.message.reply_text(response)
        return

    # Registra flussi gestionali se già in training
    if is_training and "gestionale" in message.lower():
        response = (
            "⚙️ Ricevuto anche il flusso gestionale!\n\n"
            "📈 Se vuoi aggiungere altri dettagli, continua pure.\n"
            "📬 Quando il team validerà il tutto, sarò pronto a metterlo in pratica."
        )
        save_to_sheet(user, message, response, topic, tipo="gestionale")
        await update.message.reply_text(response)
        return

    # Comando per terminare l’allenamento
    if message.lower().strip() == "fine allenamento":
        user_mode[user] = None
        response = (
            "🛠️ Allenamento terminato.\n"
            "📬 Il team validerà le istruzioni ricevute.\n"
            "🧪 Quando saranno approvate, potranno essere testate."
        )
        save_to_sheet(user, message, response, topic, tipo="chiusura")
        await update.message.reply_text(response)
        return

    # Risposte standard per chi non sta allenando
    if user not in shown_intro:
        response = (
            "🌍 Ciao! Sono Primo, l’ultimo arrivato. Mi sto allenando per aiutare con appuntamenti, clienti e problemi urgenti.\n\n"
            "🎯 Al momento mi sto concentrando sull’apprendere come gestire appuntamenti in modo perfetto, ma posso registrare qualsiasi istruzione utile all’azienda.\n\n"
            "✍️ Se vuoi insegnarmi qualcosa, inizia il messaggio con:\n‘Primo, ti insegno…’\n\n"
            "💡 Se vuoi contribuire con un’idea, scrivi:\n‘Primo, ho un’idea…’\n\n"
            "🧪 Per ora la modalità test è disattivata. Se vuoi aiutarmi a crescere, l’allenamento è la strada migliore."
        )
        shown_intro.add(user)
        await update.message.reply_text(response)
        return

    # Ultimo fallback se nessuna condizione attiva
    if is_training:
        response = (
            "📝 Ricorda che sono in modalità allenamento.\n"
            "📌 Per favore, scrivi un esempio con:\nCliente: …\nPrimo: …"
        )
        await update.message.reply_text(response)
        return

    await update.message.reply_text("💡 Per allenarmi, scrivi una frase che inizi con 'Primo, ti insegno…' oppure 'Primo, ho un’idea…'")
    return
