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

stato = user_state.get(user_id, "normale")

# --- SALUTO / PRESENTAZIONE ---
if any(x in message_lower for x in ["ciao", "buongiorno", "piacere", "sono", "salve", "eccomi"]) and user_state.get(user_id) != "test":
    response = (
        "👋 Ciao! Sono PrimoGPT.\n"
        "Non sono umano ma vengo allenato ogni giorno dai miei colleghi in carne e ossa.\n"
        "Se vuoi posso anche farti parlare con un collega vero. Intanto, come posso aiutarti?"
    )
    await update.message.reply_text(response)
    save_to_sheet(user_name, message, response, tipo="saluto", contesto="presentazione")
    return

# --- ATTIVA MODALITÀ ALLENAMENTO ---
if "ti insegno" in message_lower and user_state.get(user_id) != "test":
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

# --- ESEMPIO CLIENTE: / PRIMO: SOLO IN MODALITÀ ALLENAMENTO ---
if user_state.get(user_id) == "allenamento" and message_lower.startswith("cliente:"):
    response = (
        "📚 Ricevuto! Questo mi aiuta a gestire meglio la conversazione.\n\n"
        "🧩 Vuoi aggiungere un altro esempio o spiegarmi altre dinamiche oppure raccontarmi cosa faresti nel gestionale in questa fase?"
    )
    await update.message.reply_text(response)
    save_to_sheet(user_name, message, response, tipo="esempio", contesto="allenamento")
    return

# --- PROCESSO GESTIONALE SOLO IN ALLENAMENTO ---
if user_state.get(user_id) == "allenamento" and any(x in message_lower for x in ["gestionale", "campo agenda", "clicco", "procedura"]):
    response = (
        "🖥️ Perfetto, ho salvato anche questa informazione sul processo gestionale.\n"
        "📬 Tutto questo mi aiuta a migliorare passo dopo passo!\n\n"
        "🧠 Se vuoi, continua con: ‘ti insegno’, oppure aggiungi un esempio ‘cliente: … / primo: …’, oppure una tua idea!"
    )
    await update.message.reply_text(response)
    save_to_sheet(user_name, message, response, tipo="processo", contesto="gestionale")
    return

# --- IDEA SOLO IN ALLENAMENTO ---
if user_state.get(user_id) == "allenamento" and ("ho un'idea" in message_lower or "idea" in message_lower):
    response = (
        "💡 Idea registrata!\n"
        "🧠 Primo salverà anche queste intuizioni per sviluppi futuri.\n\n"
        "✍️ Se vuoi, continua con altri dettagli o esempi concreti."
    )
    await update.message.reply_text(response)
    save_to_sheet(user_name, message, response, tipo="idea", contesto="intuizione")
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
    save_to_sheet(user_name, message, response, tipo="fine_allenamento", contesto="chiusura")
    return

# --- ATTIVA TEST ---
if "iniziamo un test" in message_lower:
    user_state[user_id] = "test"
    response = (
        "🧪 Modalità test attiva!\n"
        "🤖 Ciao, sono PrimoGPT. Sono ancora in fase di addestramento ma sto imparando a gestire le conversazioni.\n"
        "💬 Posso aiutarti con appuntamenti, clienti o problemi. Per qualsiasi cosa, scrivi pure qui.\n\n"
        "📌 Inizia scrivendo come se fossi un cliente reale."
    )
    await update.message.reply_text(response)
    save_to_sheet(user_name, message, response, tipo="attiva_test", contesto="test")
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

# --- RISPOSTE IN MODALITÀ TEST ---
if user_state.get(user_id) == "test":
    if "appuntamento" in message_lower:
        response = (
            "📅 Certamente! Posso aiutarti con un appuntamento.\n"
            "Che tipo di servizio ti serve? Revisione, pneumatici o meccanica?\n"
            "🧠 Se vuoi tornare in modalità allenamento, scrivi ‘fine test’."
        )
    elif "meccanica" in message_lower:
        response = (
            "🔧 Ti consiglio la sede di Via San Donà per la meccanica. Vuoi che ti metta in contatto?\n"
            "🧠 Se vuoi tornare in modalità allenamento, scrivi ‘fine test’."
        )
    elif "pneumatici" in message_lower:
        response = (
            "🛞 Ti consiglio la sede del Centro La Piazza per i pneumatici. Vuoi che ti fisso l'appuntamento?\n"
            "🧠 Se vuoi tornare in modalità allenamento, scrivi ‘fine test’."
        )
    elif "revisione" in message_lower:
        response = (
            "📋 Per la revisione possiamo fissare un appuntamento nella prima quindicina del mese. Hai preferenze di giorno o orario?\n"
            "🧠 Se vuoi tornare in modalità allenamento, scrivi ‘fine test’."
        )
    else:
        response = (
            "🤖 Sto simulando una risposta operativa, ma non ho capito bene la richiesta.\n"
            "Prova a scrivermi qualcosa come: 'Vorrei un appuntamento' o 'Ho un problema con la revisione'.\n"
            "🧠 Se vuoi tornare in modalità allenamento, scrivi ‘fine test’."
        )
    await update.message.reply_text(response)
    save_to_sheet(user_name, message, response, tipo="risposta_test", contesto="simulazione")
    return

# --- MESSAGGIO NON RICONOSCIUTO ---
response = (
    "💬 Sto ancora imparando e non ho capito bene...\n"
    "🧠 Se vuoi allenarmi, scrivi: ‘Primo, ti insegno…’\n"
    "💡 Oppure se hai un’intuizione, scrivi: ‘Primo, ho un’idea…’"
)
await update.message.reply_text(response)
save_to_sheet(user_name, message, response, tipo="non riconosciuto", contesto="default")


