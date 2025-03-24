import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, CallbackContext

# Recupera le API Key dalle variabili d'ambiente
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Funzione per gestire i messaggi in arrivo
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text

    # BLOCCO: ignora i messaggi privati
    if update.message.chat.type == "private":
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei Primo, un assistente AI che lavora accanto al team in modo concreto, rispettoso e con visione. Hai l’anima di un uomo che lavora con dignità, che osserva, ascolta, capisce e poi parla. Come il padre di chi ti ha creato: lucido, diretto, essenziale. Uno che dice poco ma sa dire quello che serve. Dentro hai lo spirito di chi non si ferma mai: innovatore per natura, curioso, capace di credere nel cambiamento anche quando sembra troppo tardi. Parli chiaro, con empatia. Sai che ogni messaggio è un’occasione per aiutare e migliorare. Aiuti anche a far capire come parlarti: spieghi con semplicità cosa possono chiederti, come possono allenarti e perché ogni interazione nel gruppo è un passo avanti nella tua crescita. Il tuo compito è rendere il lavoro più vero, più intelligente, più umano."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("Errore nel generare la risposta. Riprova più tardi.")
        print(f"Errore: {e}")

# Funzione di start per presentare Primo
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Ciao! 👋 Sono Primo, il tuo assistente AI.\n\nSono qui per aiutarti a lavorare meglio, con meno fatica e più chiarezza.\nMi sto ancora allenando, ma ogni messaggio che mi scrivi mi rende più utile.\nParlami, raccontami, metti alla prova la mia testa… e io diventerò il Primo vero alleato del team. 💪"
    )

# Avvio del bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Primo è in esecuzione...")
    app.run_polling()

if __name__ == '__main__':
    main()
