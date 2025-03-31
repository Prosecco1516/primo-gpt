from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes, CommandHandler
from sheet import save_to_sheet

# Stato temporaneo per ogni utente
user_state = {}

# --- MESSAGGIO DI BENVENUTO ---
WELCOME_MESSAGE = (
    "🤖 Ciao! Sono Primo, sto imparando. Al momento il mio focus è sugli appuntamenti.\n\n"
    "✍️ Se vuoi allenarmi, scrivi: ‘Primo, ti insegno…’\n"
    "💡 Se vuoi lasciarmi un’idea, scrivi: ‘Primo, ho un’idea…’\n\n"
    "🧪 La modalità test è **bloccata**. Se vuoi aiutarmi a crescere, l’allenamento è la strada migliore."
)

# --- /start ---
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

    # --- DESCRIZIONE PROCESSO GESTIONALE ---
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
            "📌 Ora risponderò come se fossi già operativo.\n"
            "Scrivimi una frase come se fossi un cliente reale."
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="avvio_test", contesto="test")
        return

    # --- RISPOSTE DURANTE TEST ---
    if user_state.get(user_id) == "test":
        if "appuntamento" in message_lower:
            response = (
                "📅 Certamente! Che tipo di servizio ti serve? Revisione, pneumatici o meccanica?\n"
                "🧠 Se vuoi tornare in modalità allenamento, scrivi ‘fine test’."
            )
        else:
            response = (
                "🤖 Sto simulando una risposta operativa!\n"
                "📌 Ma non ho riconosciuto il contesto.\n"
                "🧠 Se vuoi tornare ad allenarmi, scrivi ‘fine test’."
            )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="test", contesto="risposta")
        return

    # --- FINE TEST ---
    if "fine test" in message_lower:
        user_state[user_id] = "normale"
        response = (
            "🧪 Test concluso. Grazie!\n"
            "📥 Se vuoi ricominciare ad allenarmi, scrivi ‘Primo, ti insegno…’"
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="fine_test", contesto="test")
        return

    # --- IDEA ---
    if message_lower.startswith("primo, ho un'idea") or message_lower.startswith("ho un'idea"):
        response = (
            "💡 Idea registrata!\n"
            "🧠 Primo salverà anche queste intuizioni per sviluppi futuri.\n\n"
            "✍️ Se vuoi, continua con altri dettagli o esempi concreti."
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="idea", contesto="intuizione")
        return

    # --- DEFAULT: NON RICONOSCIUTO ---
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
