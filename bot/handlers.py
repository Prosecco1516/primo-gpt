from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bot.funzioni import determina_sede

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono Primo 🤖. Come posso aiutarti oggi?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    SHEET_ENABLED = context.bot_data.get("SHEET_ENABLED", False)
    sheet = context.bot_data.get("sheet")

    if "appuntamento" in user_message.lower():
        sede = determina_sede(user_message)
        if sede != "Non specificato":
            reply_text = (
                f"Perfetto! Da quanto mi hai scritto, il servizio riguarda la sede *{sede}*\n"
                "Posso chiederti:\n- Nome\n- Cognome\n- Cellulare\n- Tipo di servizio esatto?\n\n"
                "Così ti aiuto a fissare l'appuntamento giusto 🚀"
            )
        else:
            reply_text = (
                "Perfetto! Ti aiuto a fissare l’appuntamento. Prima dimmi:\n"
                "- Che tipo di servizio ti serve? (es. gomme, meccanica, lucidatura...)\n"
                "In base a quello ti indirizzo nella sede corretta."
            )
        await update.message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)
        return

    if "come stai" in user_message.lower():
        await update.message.reply_text("Sto alla grande, grazie che me lo chiedi! Se hai bisogno di aiuto per un appuntamento o un dubbio tecnico, sono qui ✌️")
        return

    if user_message.lower().startswith("istruzione"):
        if SHEET_ENABLED and sheet:
            try:
                sheet.append_row([
                    str(update.message.date),
                    update.message.from_user.full_name,
                    user_message
                ])
                await update.message.reply_text("📝 Istruzione salvata su Google Sheet!")
            except Exception as e:
                await update.message.reply_text(f"⚠️ Errore nel salvataggio su Sheet: {e}")
        else:
            await update.message.reply_text("⚠️ Google Sheet non attivo. L'istruzione non è stata salvata.")
        return

    await update.message.reply_text("Ricevuto! ✉️ Se vuoi salvare questo messaggio come istruzione, inizia con la parola *istruzione*.", parse_mode=ParseMode.MARKDOWN)
