# handlers.py
from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes, CommandHandler
from sheet import save_to_sheet

# Stato temporaneo per ogni utente
user_state = {}

# --- RISPOSTE BASE ---
WELCOME_MESSAGE = (
    "🤖 Ciao! Sono Primo, l’ultimo arrivato. Mi sto allenando per aiutare con appuntamenti, clienti e problemi urgenti.\n\n"
    "🎯 Al momento mi sto concentrando sull’apprendere come gestire appuntamenti in modo perfetto, ma posso registrare qualsiasi istruzione utile all’azienda.\n\n"
    "✍️ Se vuoi insegnarmi qualcosa, inizia il messaggio con:\n‘Primo, ti insegno…’\n\n"
    "💡 Se vuoi contribuire con un’idea, scrivi:\n‘Primo, ho un’idea…’\n\n"
    "🧪 Per ora la modalità test è disattivata. Se vuoi aiutarmi a crescere, l’allenamento è la strada migliore."
)

# --- HANDLER DI PARTENZA ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

# --- MESSAGGI ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user = update.message.from_user
    user_id = user.id
    chat_type = update.message.chat.type

    # Salva nome utente e messaggio originale
    user_name = user.full_name

    # Attiva allenamento
    if message.lower().startswith("primo, ti insegno"):
        user_state[user_id] = "allenamento"
        response = (
            "🧠 Ok, sono in modalità allenamento.\n"
            "📥 Sto registrando le istruzioni che riceverò.\n"
            "✅ Se saranno approvate, diventeranno parte delle mie risposte ufficiali.\n\n"
            "✍️ Ora, se vuoi aiutarmi davvero, scrivimi un esempio così:\n"
            "Cliente: cosa dice?\nPrimo: come dovrei rispondere?"
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="istruzione", contesto="avvio allenamento")
        return

    # Se l'utente è in allenamento e scrive un esempio
    if user_state.get(user_id) == "allenamento" and message.lower().startswith("cliente:"):
        response = (
            "📚 Ricevuto! Questo mi aiuta a gestire meglio la conversazione.\n\n"
            "💡 Vuoi aggiungere un altro esempio oppure approfondire come continua la conversazione con il cliente?\n"
            "Puoi anche dirmi cosa fai tu nel gestionale in questo caso."
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="esempio", contesto="allenamento")
        return

    # Chiude allenamento
    if "fine allenamento" in message.lower():
        user_state[user_id] = "normale"
        response = (
            "🛠️ Allenamento terminato.\n"
            "📬 Il team validerà le istruzioni ricevute.\n"
            "🧪 Quando saranno approvate, potranno essere testate.\n\n"
            "Se vuoi riprendere, scrivi: ‘Primo, ti insegno…’"
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="chiusura", contesto="fine allenamento")
        return

    # Accoglie idee
    if message.lower().startswith("primo, ho un'idea") or message.lower().startswith("ho un'idea"):
        response = (
            "💡 Idea registrata!\n"
            "🧠 Primo salverà anche queste intuizioni per sviluppi futuri.\n\n"
            "✍️ Se vuoi, continua con altri dettagli o esempi concreti."
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="idea", contesto="intuizione")
        return

    # Risposta generica e stimolante se non capisce il contesto
    response = (
        "💡 Non sono sicuro di aver capito...\n"
        "🧠 Vuoi aiutarmi ad allenarmi? Scrivi una frase che inizi con ‘Primo, ti insegno…’\n\n"
        "📌 Oppure se hai un’intuizione, scrivi: ‘Primo, ho un’idea…’"
    )
    await update.message.reply_text(response)
    save_to_sheet(user_name, message, response, tipo="generico", contesto="non riconosciuto")

# Handler Telegram
start_handler = CommandHandler("start", start)
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
