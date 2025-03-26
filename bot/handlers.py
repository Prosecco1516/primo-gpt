from telegram.ext import CommandHandler, MessageHandler, filters

async def start_command(update, context):
    await update.message.reply_text("Ciao! Sono PrimoGPT 🤖")

async def handle_message(update, context):
    text = update.message.text
    await update.message.reply_text(f"Hai scritto: {text}")

start_handler = CommandHandler("start", start_command)
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
