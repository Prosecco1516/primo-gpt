from telegram.ext import CommandHandler, MessageHandler, filters

def start_command(update, context):
    update.message.reply_text("Ciao! Sono PrimoGPT 🤖")

def handle_message(update, context):
    text = update.message.text
    update.message.reply_text(f"Hai scritto: {text}")

# Questi sono gli handler da esportare nel main
start_handler = CommandHandler("start", start_command)
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
