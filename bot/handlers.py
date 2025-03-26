from telegram.ext import CommandHandler, MessageHandler, filters

start_handler = CommandHandler("start", start_command)  # start_command è una funzione
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)  # handle_message è una funzione
