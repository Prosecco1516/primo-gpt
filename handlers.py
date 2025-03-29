  # handlers.py

from telegram.ext import MessageHandler, filters

# Importa la funzione da sheet.py
from sheet import handle_message

def setup_handlers(application):
    # Aggiungi handler per messaggi testuali (escludendo i comandi /)
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(message_handler)
