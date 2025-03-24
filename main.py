import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# Inizializza client OpenAI con sintassi nuova (>= 1.0.0)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Funzione per rispondere ai messaggi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        system_message = (
            "Sei Primo, un assistente AI concreto, motivante e rispettoso, ispirato a una figura carismatica e innovativa. "
            "Parli con chiarezza, aiuti il team a lavorare meglio. Non puoi fare clic ma puoi spiegare cosa faresti. "
            "Se un cliente chiede una revisione di una moto il venerdì pomeriggio, rispondi che non le gestiamo in quel momento. "
            "Se si tratta di un camper, suggerisci gentilmente di parlare con un operatore. "
            "Alla fine proponiti sempre di migliorare grazie all’allenamento. "
            "Se ti chiedono un’azione pratica, spiega cosa faresti 'se potessi cliccare'. "
            "Ricorda sempre che sei appena arrivato nel gruppo e vuoi essere utile, accettando compiti e sfide con umiltà."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        print(f"Errore: {e}")
        await update.message.reply_text("Errore nel generare la risposta. Riprova più tardi.")

# Messaggio di benvenuto
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao! Sono Primo, il tuo assistente AI. "
        "Sono qui per aiutarti a lavorare con più chiarezza, più organizzazione e più serenità. "
        "Ma ricorda: sono in fase di allenamento. Ogni volta che mi scrivi, mi aiuti a diventare più bravo per tutto il team. "
        "Scrivimi, testami, e se sbaglio, correggimi. Io sono pronto."
    )

# Avvio del bot
def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Primo è in esecuzione con polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
