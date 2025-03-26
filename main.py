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
    salva_istruzione = context.bot_data.get("salva_istruzione")
    risposta_finale = None

    if "appuntamento" in user_message.lower():
        sede = determina_sede(user_message)
        if sede != "Non specificato":
            risposta_finale = (
                f"Perfetto! Da quanto mi hai scritto, il servizio riguarda la sede *{sede}*\n"
                "Posso chiederti:\n- Nome\n- Cognome\n- Cellulare\n- Tipo di servizio esatto?\n\n"
                "Così ti aiuto a fissare l'appuntamento giusto 🚀"
            )
        else:
            risposta_finale = (
                "Perfetto! Ti aiuto a fissare l’appuntamento. Prima dimmi:\n"
                "- Che tipo di servizio ti serve? (es. gomme, meccanica, lucidatura...)\n"
                "In base a quello ti indirizzo nella sede corretta."
            )
        await update.message.reply_text(risposta_finale, parse_mode=ParseMode.MARKDOWN)

    elif "come stai" in user_message.lower():
        risposta_finale = "Sto alla grande, grazie che me lo chiedi! Se hai bisogno di aiuto per un appuntamento o un dubbio tecnico, sono qui ✌️"
        await update.message.reply_text(risposta_finale)

    else:
        risposta_finale = "Ricevuto! ✉️ Se vuoi salvare questo messaggio come istruzione, inizia con la parola *istruzione*."
        await update.message.reply_text(risposta_finale, parse_mode=ParseMode.MARKDOWN)

    # Salvataggio solo se è un'istruzione
    if "istruzione" in user_message.lower() and SHEET_ENABLED and salva_istruzione:
        await salva_istruzione(sheet, update.message.from_user.full_name, user_message, risposta_finale)
