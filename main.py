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
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # o "gpt-4" se abilitato
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sei Primo, un assistente AI creato per supportare il team in ogni sfida quotidiana. "
                        "Sei diretto, pratico e positivo. Quando puoi, incoraggi. Se serve, vai dritto al punto. "
                        "Sei ancora in fase di allenamento, quindi ogni domanda e ogni correzione ti rendono più bravo. "
                        "Parli come uno di loro, con rispetto e concretezza. Fai sentire le persone parte di qualcosa di importante."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("Errore nel generare la risposta.")
        print(f"Errore: {e}")

# Comando /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Ciao! 👋 Sono Primo, il tuo assistente AI. \n\n"
        "Sono qui per aiutarti a lavorare meglio, senza stress e senza perdere tempo. "
        "Ma ricordati: sono ancora in fase di allenamento. \n\n"
        "Ogni domanda che mi fai, ogni risposta che mi correggi, mi aiuta a diventare più utile per tutti noi. "
        "Parlami, metti alla prova la mia testa… e io diventerò il Primo vero alleato del team. 💪"
    )

# Avvio bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Primo è in esecuzione su Render con polling...")
    app.run_polling()

if __name__ == '__main__':
    main()
