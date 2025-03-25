import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes
from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === CONFIGURAZIONI ===

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Inserisci qui l’ID del tuo Google Sheet
SHEET_ID = "109018550274954569288"  # <-- cambia questo

# === FUNZIONE DI SALVATAGGIO SU GOOGLE SHEETS ===

def salva_su_google_sheets(nome, messaggio):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("primogpt-454723-605ef4487970.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1
    sheet.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nome, messaggio])

# === GESTIONE MESSAGGI ===

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_type = update.message.chat.type
    user_name = update.message.from_user.first_name

    # Se è una chat privata, blocchiamo
    if chat_type == "private":
        await update.message.reply_text("Per ora possiamo parlare solo nel gruppo, ci vediamo lì!")
        return

    # Se qualcuno chiede “come stai primo?”
    if "come stai" in user_message.lower() and "primo" in user_message.lower():
        await update.message.reply_text(
            f"Oggi alla grande! Se hai urgenze ti passo qualcuno, altrimenti sono qui per ascoltarti, {user_name}."
        )
        return

    # Se qualcuno scrive “salva questo”
    if "salva questo" in user_message.lower():
        salva_su_google_sheets(user_name, user_message)
        await update.message.reply_text("Messaggio salvato! Primo sta imparando.")
        return

    # Prompt per GPT
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei Primo, un assistente AI concreto e positivo, motivato ad aiutare il team a lavorare meglio. Sei umile e vuoi migliorare l'ambiente. Quando puoi, dai una mano. Se ti parlano di appuntamenti, chiedi nome, cognome, cellulare e tipo di servizio (revisione, pneumatici, meccanica). Se è una revisione, e si tratta di moto il venerdì pomeriggio, avvisa che non le facciamo. Se è un camper, passa la palla a un operatore."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Errore nel generare la risposta. Riprova più tardi.")
        print(f"Errore: {e}")

# === COMANDO /start ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao! Sono Primo, il tuo nuovo assistente AI. Sono qui per aiutarti a risparmiare tempo, lavorare meglio e vivere più sereni. Sono ancora in fase di allenamento: ogni messaggio mi rende più utile. Scrivimi pure… e se vuoi salvarmi qualcosa, scrivi 'salva questo'."
    )

# === AVVIO BOT ===

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Primo è in esecuzione...")
    app.run_polling()

if __name__ == "__main__":
    main()
