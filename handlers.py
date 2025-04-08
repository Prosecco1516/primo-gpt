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
    if any(x in message_lower for x in ["ciao primo", "come va", "primo!", "buongiorno", "pronto", "sono", "eccomi"]):
        response = (
            "🤖 Ciao, sono PrimoGPT. Sono ancora in fase di addestramento ma sto imparando a gestire le conversazioni.\n"
            "💬 Posso aiutarti con appuntamenti, clienti o problemi. Per qualsiasi cosa, scrivi pure qui.\n\n"
            "✍️ Se vuoi insegnarmi qualcosa, inizia con: ‘Primo, ti insegno…’ oppure scrivimi un esempio con:\n"
            "Cliente: …\nPrimo: …"
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="saluto", contesto="iniziale")
        return

    # --- FINE TEST ---
    if "fine test" in message_lower:
        user_state[user_id] = "allenamento"
        response = (
            "🧪 Test concluso. Grazie!\n"
            "📥 Torno in modalità allenamento: puoi riprendere con ‘Primo, ti insegno…’"
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="fine_test", contesto="test")
        return

    # --- TEST MODE ---
    if user_state.get(user_id) == "test":
        if "appuntamento" in message_lower:
            response = (
                "🤖 Ciao, sono PrimoGPT. Mi sto addestrando per aiutare con appuntamenti e gestione clienti.\n"
                "📅 Vuoi fissare un appuntamento? Che tipo di servizio ti serve? Pneumatici, revisione o meccanica?\n"
                "🧠 Scrivi ‘fine test’ per tornare in modalità allenamento."
            )
        elif "meccanica" in message_lower:
            response = (
                "🔧 Ti consiglio la sede di Via San Donà per la meccanica. Vuoi che ti metta in contatto?\n"
                "🧠 Scrivi ‘fine test’ per tornare in modalità allenamento."
            )
        elif "pneumatici" in message_lower:
            response = (
                "🛞 Ti consiglio la sede del Centro La Piazza per i pneumatici. Vuoi che ti fisso l'appuntamento?\n"
                "🧠 Scrivi ‘fine test’ per tornare in modalità allenamento."
            )
        elif "revisione" in message_lower:
            response = (
                "📋 Per la revisione possiamo fissare un appuntamento nella prima quindicina del mese. Hai preferenze di giorno o orario?\n"
                "🧠 Scrivi ‘fine test’ per tornare in modalità allenamento."
            )
        else:
            response = (
                "🤖 Sto simulando una risposta operativa, ma non ho capito bene la richiesta.\n"
                "Prova con: 'Vorrei un appuntamento' o 'Ho un problema'.\n"
                "🧠 Scrivi ‘fine test’ per tornare in modalità allenamento."
            )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="test", contesto="risposta")
        return

    # --- AVVIO TEST ---
    if "iniziamo un test" in message_lower:
        user_state[user_id] = "test"
        response = (
            "🧪 Modalità test attiva!\n"
            "🤖 Ciao, sono PrimoGPT. Sono ancora in fase di addestramento ma sto imparando.\n"
            "💬 Posso aiutarti con appuntamenti, clienti o problemi. Prova a scrivermi come se fossi un cliente reale!"
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="avvio_test", contesto="test")
        return

    # --- BLOCCA ALLENAMENTO DURANTE IL TEST ---
    if user_state.get(user_id) == "test" and any(x in message_lower for x in ["ti insegno", "cliente:", "gestionale", "ho un'idea", "idea"]):
        response = (
            "⛔ Attualmente sono in modalità test. Non posso essere allenato ora.\n"
            "🧪 Scrivi ‘fine test’ per tornare in modalità allenamento."
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="errore", contesto="istruzione in test")
        return

    # --- AVVIO ALLENAMENTO ---
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

    # --- DESCRIZIONE GESTIONALE ---
    if user_state.get(user_id) == "allenamento" and any(x in message_lower for x in ["gestionale", "clicco", "campo agenda", "procedura"]):
        response = (
            "🖥️ Perfetto, ho salvato anche questa informazione sul processo gestionale.\n"
            "📬 Tutto questo mi aiuta a migliorare passo dopo passo!\n\n"
            "🧠 Se vuoi, continua con: ‘ti insegno’, oppure aggiungi un esempio ‘cliente: … / primo: …’, oppure una tua idea!"
        )
        await update.message.reply_text(response)
        save_to_sheet(user_name, message, response, tipo="processo", contesto="gestionale")
        return

    # --- IDEA ---
    if message_lower.startswith("primo, ho un'idea") or message_lower.startswith("ho un'idea") or "idea" in message_lower:
        if user_state.get(user_id) == "test":
            response = (
                "⛔ Attualmente sono in modalità test. Non posso registrare nuove idee.\n"
                "🧠 Scrivi ‘fine test’ per tornare in allenamento."
            )
        else:
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
