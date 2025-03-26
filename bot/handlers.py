# handlers.py
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono PrimoGPT 🤖")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Hai scritto: {text}")

start_handler = CommandHandler("start", start_command)
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
