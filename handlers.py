# handlers.py
from telegram.ext import MessageHandler, filters
from sheet import handle_message

start_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
