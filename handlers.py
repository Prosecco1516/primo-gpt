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

# --- ESEMPIO IN FORMATO LIBERO ---
if user_state.get(user_id) == "allenamento" and "cliente:" in message_lower and "primo:" in message_lower:
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

# --- FINE TEST (torna in modalità allenamento) ---
if "fine test" in message_lower:
    user_state[user_id] = "allenamento"
    response = (
        "🧪 Test concluso. Grazie!\n"
        "📥 Torno in modalità allenamento!\n"
        "Scrivimi pure un'istruzione o un esempio."
    )
    await update.message.reply_text(response)
    save_to_sheet(user_name, message, response, tipo="fine_test", contesto="test")
    return

# --- IDEA ---
if "idea" in message_lower:
    response = (
        "💡 Idea registrata!\n"
        "🧠 Primo salverà anche queste intuizioni per sviluppi futuri.\n\n"
        "✍️ Se vuoi, continua con altri dettagli o esempi concreti."
    )
    await update.message.reply_text(response)
    save_to_sheet(user_name, message, response, tipo="idea", contesto="intuizione")
    return

# --- DEFAULT ---
response = (
    "💬 Sto ancora imparando e non ho capito bene...\n"
    "🧠 Se vuoi allenarmi, scrivi: ‘Primo, ti insegno…’\n"
    "💡 Oppure se hai un’intuizione, scrivi: ‘Primo, ho un’idea…’"
)
await update.message.reply_text(response)
save_to_sheet(user_name, message, response, tipo="generico", contesto="non riconosciuto")
