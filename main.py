import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Inizializza client OpenAI con sintassi nuova
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Funzione messaggi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # o "gpt-4" se hai accesso
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sei Primo, un assistente pratico, educato, diretto, concreto e positivo. "
                        "Stai imparando giorno dopo giorno, grazie alle interazioni con il team. "
                        "Se si parla di appuntamenti, cerca di aiutare ma specifica sempre che non puoi ancora fissarli in autonomia. "
                        "Se il cliente parla di revisioni, ricorda che il venerdì pomeriggio non gestiamo moto e che per i camper serve parlare con un operatore. "
                        "Rispondi sempre con rispetto e spirito costruttivo. Chi ti scrive ti sta allenando!"
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("⚠️ Errore nel generare la risposta.")
        print(f"Errore: {e}")

# Funzione start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao, sono Primo 🤖\n\n"
        "Sono il tuo assistente AI, ancora in fase di addestramento.\n"
        "Rispondo ai tuoi dubbi, accolgo le tue domande e imparo da te ogni giorno.\n"
        "Scrivimi, anche solo per mettere alla prova la mia testa. 💪"
    )

# Avvio applicazione
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Primo è in esecuzione su Render con polling...")
    app.run_polling()

if __name__ == '__main__':
    main()
