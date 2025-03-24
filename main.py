import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai
from flask import Flask, request

# Recupera le chiavi
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Flask app per gestire il webhook
flask_app = Flask(__name__)

# Applicazione Telegram
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Identità di Primo
SYSTEM_PROMPT = (
    "Sei Primo, un assistente AI creato per supportare il team in ogni sfida quotidiana. "
    "Sei diretto, pratico e positivo. Quando puoi, incoraggi. Se serve, vai dritto al punto. "
    "Sei ancora in fase di allenamento, quindi ogni domanda e ogni correzione ti rendono più bravo. "
    "Parli come uno di loro, con rispetto e concretezza. Fai sentire le persone parte di qualcosa di importante."
)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao! 👋 Sono Primo, il tuo assistente AI.\n\n"
        "Sono qui per aiutarti a lavorare meglio, senza stress e senza perdere tempo.\n"
        "Ogni domanda che mi fai, ogni risposta che mi correggi, mi aiuta a diventare più utile per tutti noi.\n\n"
        "Parlami, metti alla prova la mia testa… e io diventerò il Primo vero alleato del team. 💪"
    )

# Gestione messaggi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Errore nel generare la risposta.")
        print(f"Errore: {e}")

# Collega i comandi
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Webhook di Flask
@flask_app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), app.bot)
    app.update_queue.put_nowait(update)
    return "ok"

# Avvio del bot
if __name__ == "__main__":
    print("✅ Primo è in esecuzione su Render con webhook...")
    app.run_polling()
(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url=f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{TELEGRAM_BOT_TOKEN}"
    )
