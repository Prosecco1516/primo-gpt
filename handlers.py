from telegram.ext import CommandHandler, MessageHandler, filters
from sheet import handle_message

def start_command(update, context):
    update.message.reply_text("Ciao! Sono PrimoGPT 🤖")

start_handler = CommandHandler("start", start_command)
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
