# handlers.py
from telegram.ext import MessageHandler, CommandHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from sheet import handle_message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono Primo, pronto ad aiutarti e ad allenarmi. Scrivimi pure.")

start_handler = CommandHandler("start", start)
message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
