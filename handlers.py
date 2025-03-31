# handlers.py
from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes, CommandHandler
from sheet import save_to_sheet

# Stato temporaneo per ogni utente
user_state = {}

# --- RISPOSTE BASE ---
WELCOME_MESSAGE = (
    "👋 Ciao! Sono Primo, sto imparando. Al momento il mio focus è sugli appuntamenti.\n"
    "✍️ Se vuoi allenarmi, scrivi: ‘Primo, ti insegno…’\n"
    "💡 Se invece vuoi lasciarmi un’idea, scrivi: ‘Primo, ho un’idea…’\n"
    "🧪 La modalità test è **bloccata**: devo ancora imparare bene! Se vuoi aiutarmi, allenami con istruzioni reali."
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

    user_name = user.full_name
    message_lower = message.lower()

    # --- SALUTO ---
    if any(phrase in message_lower for phrase in ["ciao primo", "come va", "primo!"]):
        response = WELCOME_MESSAGE
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="saluto", contesto="iniziale")
        return

    # --- ATTIVA ALLENAMENTO (MODIFICATO) ---
if "ti insegno" in message_lower:
    user_state[user_id] = "allenamento"
    response = (
        "🧠 Ok, sono in modalità allenamento.\n"
        "📥 Sto registrando le istruzioni che riceverò.\n"
        "✅ Se saranno approvate, diventeranno parte delle mie risposte ufficiali.\n"
        "✅ Ti va di continuare ad insegnarmi ancora?\n\n"
        "✍️ Oppure fammi un esempio!\n"
        "Scrivimi così:\n"
        "Cliente: cosa desidera\n"
        "Primo: come dovrei rispondere?"
    )
    await update.message.reply_text(response)
    save_to_sheet(user_name, message, response, tipo="istruzione", contesto="avvio allenamento")
    return


    # --- RICEVE ESEMPIO ---
    if user_state.get(user_id) == "allenamento" and message_lower.startswith("cliente:"):
        response = (
            "📚 Ricevuto! Questo mi aiuta a gestire meglio la conversazione.\n\n"
            "🧩 Vuoi aggiungere un altro esempio, insegnarmi un’istruzione nuova\n"
            "oppure raccontarmi cosa faresti nel gestionale in questa fase?"
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="esempio", contesto="allenamento")
        return

    # --- PROCESSO GESTIONALE ---
    if user_state.get(user_id) == "allenamento" and any(word in message_lower for word in ["gestionale", "campo agenda", "clicco", "targa"]):
        response = (
            "🖥️ Perfetto, ho salvato anche questa informazione sul processo gestionale.\n"
            "📈 Tutto questo mi aiuta a migliorare passo dopo passo!"
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="processo", contesto="gestionale")
        return

    # --- FINE ALLENAMENTO ---
    if "fine allenamento" in message_lower:
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

    # --- RICEVE IDEA ---
    if message_lower.startswith("primo, ho un'idea") or message_lower.startswith("ho un'idea"):
        response = (
            "💡 Idea registrata!\n"
            "🧠 Primo salverà anche queste intuizioni per sviluppi futuri.\n\n"
            "✍️ Se vuoi, continua con altri dettagli o esempi concreti."
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="idea", contesto="intuizione")
        return

    # --- MESSAGGIO NON RICONOSCIUTO ---
    response = (
        "💬 Sto ancora imparando e non ho capito bene...\n"
        "🧠 Se vuoi allenarmi, scrivi: ‘Primo, ti insegno…’\n"
        "📌 Oppure se hai un’intuizione o una proposta, scrivi: ‘Primo, ho un’idea…’"
    )
    await update.message.reply_text(response)
    save_to_sheet(user_name, message, response, tipo="generico", contesto="non riconosciuto")

# --- HANDLERS ---
start_handler = CommandHandler("start", start)
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
