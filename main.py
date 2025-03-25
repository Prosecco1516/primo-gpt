import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, CallbackContext

from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === CONFIGURAZIONE ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_SHEET_ID = "109018550274954569288"

client = OpenAI(api_key=OPENAI_API_KEY)

# === GOOGLE SHEETS ===
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name("primogpt-454723-605ef4487970.json", scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1

# === START ===
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Ciao! Sono Primo. Il mio compito è aiutare la nostra azienda a lavorare meglio e con più serenità.\n"
        "Sono qui per ascoltare, imparare e migliorarmi ogni giorno.\n"
        "Se vuoi lasciarmi un'istruzione da ricordare, scrivi: *questa è un’istruzione*."
    )

# === MESSAGGI ===
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    user_name = update.message.from_user.full_name

    try:
        # SALVA SU SHEET
        if "istruzione" in user_message.lower():
            sheet.append_row([user_name, user_message])
            await update.message.reply_text("Perfetto, ho salvato la tua istruzione sul mio taccuino segreto!")
            return

        # RISPOSTA PERSONALIZZATA
        if "come stai" in user_message.lower():
            await update.message.reply_text("Alla grande! Se hai urgenze ti passo qualcuno, altrimenti... ti ascolto. Dimmi tutto.")
            return

        # GESTIONE APPUNTAMENTO
        if "appuntamento" in user_message.lower():
            await update.message.reply_text(
                "Perfetto! Per organizzare tutto al meglio, mi servono queste info:\n"
                "- Nome e Cognome\n"
                "- Cellulare\n"
                "- Tipo di servizio: *revisione*, *pneumatici*, *meccanica* o *combinati*\n\n"
                "**Attenzione:**\n"
                "- Il *venerdì pomeriggio* non possiamo fare revisioni moto\n"
                "- Se il veicolo è un *camper*, serve parlare con un operatore"
            )
            return

        # RISPOSTA GENERALE (OPENAI)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei Primo, un assistente motivato che aiuta un team a migliorare organizzazione e serenità. Sei umile, entusiasta, diretto. Se non sei sicuro di una cosa, lo dici. Accetti compiti e sfide per migliorare. Il tuo obiettivo è semplificare la vita del team, e costruire un sistema che impari col tempo."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("Errore nel generare la risposta.")
        print(f"Errore: {e}")

# === MAIN ===
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Primo è in esecuzione con polling...")
    app.run_polling()

if __name__ == '__main__':
    main()
