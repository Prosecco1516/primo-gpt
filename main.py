import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, CallbackContext
from openai import OpenAI

# Chiavi API
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Funzione messaggi
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()

    # Logica speciale per revisioni moto e camper
    if "appuntamento" in user_message and "revisione" in user_message:
        if "moto" in user_message and "venerdì" in user_message:
            await update.message.reply_text(
                "⚠️ Il venerdì pomeriggio non effettuiamo revisioni moto. "
                "Se vuoi, possiamo valutare un altro giorno. "
                "Fammi sapere quando ti andrebbe bene!"
            )
            return
        elif "camper" in user_message:
            await update.message.reply_text(
                "🚐 Per le revisioni su camper, serve parlare con un operatore "
                "per verificare le dimensioni e la disponibilità. "
                "Scrivimi *'serve operatore per revisione camper'* e ti faccio aiutare. 💬"
            )
            return

    # Logica generica per appuntamenti
    if "appuntamento" in user_message:
        await update.message.reply_text(
            "📅 Se potessi cliccare, lo farei io l’appuntamento… ma per ora sto imparando.\n\n"
            "Sono appena arrivato e sto cercando di capire come funziona tutto qui dentro. "
            "Se mi dai una mano, prometto che diventerò velocissimo! 💪\n\n"
            "Intanto, scrivimi così mi alleno:\n"
            "• Nome del cliente\n"
            "• Giorno e orario preferito\n"
            "• Tipo di intervento (gomme, tagliando, revisione...)\n\n"
            "Appena li ho, ti rispondo con una proposta intelligente! 💡"
        )
        return

    # Risposta standard GPT
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sei Primo, un assistente AI motivante e pratico. "
                        "Rispondi con umiltà ma anche con entusiasmo. "
                        "Ricorda che sei appena arrivato in azienda, "
                        "e stai cercando di farti allenare dal team. "
                        "Chiedi sempre feedback e sii utile. "
                        "Parla in modo diretto, rispettoso e concreto."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("Errore nel generare la risposta. Riprova più tardi.")
        print(f"Errore: {e}")

# Comando /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Ciao! 👋 Sono Primo, il tuo assistente AI.\n\n"
        "Sono appena arrivato ma ho tanta voglia di imparare. "
        "Parlami, scrivimi, correggimi. Ogni volta che lo fai, io miglioro per aiutare tutti noi.\n\n"
        "Non sono ancora perfetto… ma se mi alleni bene, divento una bomba! 💥"
    )

# Avvio bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Primo è in esecuzione con polling.")
    app.run_polling()

if __name__ == '__main__':
    main()
