from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono Primo 🤖, pronto ad aiutarti!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"Hai scritto: {user_message}")

start_command = CommandHandler("start", start)
handle_message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
