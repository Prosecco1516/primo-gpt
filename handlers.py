# handlers.py
from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes, CommandHandler
from sheet import save_to_sheet

# Stato temporaneo per ogni utente
user_state = {}

# --- MESSAGGIO DI BENVENUTO ---
WELCOME_MESSAGE = (
    "🤖 Ciao! Sono Primo, sto imparando. Il mio focus è sugli appuntamenti, ma ogni giorno allargo le mie competenze.\n\n"
    "🧠 Per aiutarmi, puoi:\n"
    "✍️ Scrivere un’istruzione così: ‘Primo, ti insegno…’\n"
    "💡 Lasciarmi un’intuizione così: ‘Primo, ho un’idea…’\n\n"
    "🧪 La modalità test è bloccata. Continua ad allenarmi!"
)

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

# --- HANDLE MESSAGE ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user = update.message.from_user
    user_id = user.id
    user_name = user.full_name
    message_lower = message.lower()

    # --- SALUTO ---
    if any(x in message_lower for x in ["ciao primo", "come va", "primo!"]):
        response = WELCOME_MESSAGE
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="saluto", contesto="iniziale")
        return

    # --- ATTIVA ALLENAMENTO ---
    if "ti insegno" in message_lower:
        user_state[user_id] = "allenamento"
        response = (
            "🧠 Ok, sono in modalità allenamento.\n"
            "📥 Sto registrando le istruzioni che riceverò.\n"
            "✅ Se saranno approvate, diventeranno parte delle mie risposte ufficiali.\n"
            "✅ Ti va di continuare ad insegnarmi ancora?\n\n"
            "✍️ Oppure fammi un esempio!\n"
            "Scrivimi così:\nCliente: cosa desidera\nPrimo: come dovrei rispondere?"
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="istruzione", contesto="avvio allenamento")
        return

    # --- RICEVE ESEMPIO ---
    if user_state.get(user_id) == "allenamento" and message_lower.startswith("cliente:"):
        response = (
            "📚 Ricevuto! Questo mi aiuta a gestire meglio la conversazione.\n\n"
            "🧩 Vuoi aggiungere un altro esempio o spiegarmi altre dinamiche oppure raccontarmi cosa faresti nel gestionale in questa fase?"
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="esempio", contesto="allenamento")
        return

    # --- PROCESSO GESTIONALE ---
    if user_state.get(user_id) == "allenamento" and any(x in message_lower for x in ["gestionale", "clicco", "campo agenda", "procedura"]):
        response = (
            "🖥️ Perfetto, ho salvato anche questa informazione sul processo gestionale.\n"
            "📬 Tutto questo mi aiuta a migliorare passo dopo passo!\n\n"
            "🧠 Se vuoi, continua con: ‘ti insegno’, oppure aggiungi un esempio ‘cliente: … / primo: …’, oppure una tua idea!"
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
            "Per ricominciare: ‘Primo, ti insegno…’"
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="chiusura", contesto="fine allenamento")
        return

    # --- AVVIO TEST ---
    if "iniziamo un test" in message_lower:
        user_state[user_id] = "test"
        response = (
            "🧪 Modalità test attiva!\n"
            "🤖 Ricorda che sono ancora in fase di apprendimento.\n\n"
            "📌 Proverò a rispondere come se fossi già operativo.\n"
            "Scrivimi come se fossi un cliente reale.\n"
            "📎 E se vuoi tornare in allenamento, scrivi ‘fine test’."
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="avvio_test", contesto="test")
        return

    # --- DURANTE IL TEST ---
    if user_state.get(user_id) == "test":
        if "appuntamento" in message_lower:
            response = (
                "📞 Buongiorno! Sono Primo, il primo assistente AI dell’officina. Sto imparando a gestire le richieste come questa.\n"
                "📅 Che tipo di appuntamento desideri? Revisione, pneumatici o meccanica?\n"
                "📎 Se in futuro vuoi parlare con un collega umano, potrai farlo, ma fidati: io sono allenato proprio da loro."
            )
        else:
            response = (
                "🤖 Sto simulando una risposta operativa!\n"
                "🔎 Non ho ancora imparato bene a gestire questa richiesta.\n"
                "📥 Vuoi allenarmi? Scrivi: ‘Primo, ti insegno…’"
            )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="test", contesto="risposta")
        return

    # --- FINE TEST ---
    if "fine test" in message_lower:
        user_state[user_id] = "allenamento"
        response = (
            "🧪 Test concluso. Grazie!\n"
            "🎯 Sono tornato in modalità allenamento. Vuoi continuare con ‘Primo, ti insegno…’?"
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="fine_test", contesto="test")
        return

    # --- IDEA ---
    if "ho un'idea" in message_lower or "primo, ho un'idea" in message_lower:
        response = (
            "💡 Idea registrata!\n"
            "🧠 Primo salverà anche queste intuizioni per sviluppi futuri.\n\n"
            "✍️ Se vuoi, continua con altri dettagli o esempi concreti!"
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="idea", contesto="intuizione")
        return

    # --- MESSAGGIO NON RICONOSCIUTO ---
    response = (
        "💬 Sto ancora imparando e non ho capito bene...\n"
        "🧠 Se vuoi allenarmi, scrivi: ‘Primo, ti insegno…’\n"
        "💡 Oppure se hai un’intuizione, scrivi: ‘Primo, ho un’idea…’"
    )
    await update.message.reply_text(response)
    save_to_sheet(user_name, message, response, tipo="generico", contesto="non riconosciuto")

# --- EXPORT HANDLER ---
start_handler = CommandHandler("start", start)
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)


