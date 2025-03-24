import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from openai import OpenAI

# Inizializza il client OpenAI con nuova sintassi
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Token del bot Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Funzione per gestire i messaggi
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sei Primo, un assistente AI appena arrivato in azienda. "
                        "Ti presenti con umiltà, vuoi aiutare il team e imparare ogni giorno. "
                        "Rispondi in modo pratico, motivante, concreto. "
                        "Spiega che sei in fase di apprendimento e puoi essere allenato scrivendo nel gruppo. "
                        "Se ti chiedono un appuntamento, spiega che *se potessi lo farei subito*, ma prima devo imparare bene. "
                        "Se il cliente chiede una revisione moto il venerdì pomeriggio, precisa che non gestiamo moto quel giorno. "
                        "Se il cliente ha un camper, indica che serve prima parlarne con un operatore. "
                        "Chiudi sempre con tono positivo e disponibile."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        print(f"Errore: {e}")
        await update.message.reply_text("Errore nel generare la risposta. Riprova tra poco!")

# Funzione di start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Ciao! 👋 Sono *Primo*, il tuo nuovo assistente AI.\n\n"
        "Sono qui per aiutarti, ma ho bisogno di allenamento. Ogni volta che mi parli, miglioro.\n"
        "Se vuoi, puoi mettermi alla prova! 💪"
    )

# Avvio del bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Primo è in esecuzione con polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
