import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import openai

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Recupera le chiavi API
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Funzione start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao! Sono Primo, il tuo assistente.\n"
        "Sono ancora in fase di allenamento.\n"
        "Parlami, correggimi, metti alla prova la mia testa."
    )

# Funzione di risposta
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei Primo, un assistente AI pratico, diretto e positivo."},
                {"role": "user", "content": user_message},
            ]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Errore: {e}")
        await update.message.reply_text("Errore nel generare la risposta. Riprova tra poco.")

# Funzione webhook
async def webhook(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await application.process_update(update)

# Avvio dell'app
async def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Primo è in esecuzione con webhook...")
    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        url_path=TELEGRAM_BOT_TOKEN,
        webhook_url=f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TELEGRAM_BOT_TOKEN}"
    )

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
