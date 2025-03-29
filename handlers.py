    # Blocchi di testo di saluto generici
    saluti_generici = ["ciao", "come va", "ci sei", "primo?", "ehi", "buongiorno", "buonasera", "salve", "hey"]

    # Se il messaggio è un saluto e utente non ha ancora ricevuto l’intro
    if any(parola in message.lower() for parola in saluti_generici) and user not in shown_intro:
        response = (
            "🤖 Primo | Sono l’ultimo arrivato e sto imparando! "
            "In questo periodo mi sto concentrando sugli appuntamenti e sulle telefonate. "
            "Se vuoi darmi una mano, scrivi 'Primo ti insegno' oppure raccontami una situazione vera da cui posso imparare."
        )
        await update.message.reply_text(response)
        shown_intro.add(user)
        return
