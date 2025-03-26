# main.py
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.handlers import start_command, handle_message

def main():
    application = ApplicationBuilder().token("8108284075:AAHs2urWXlt0sGzXG2EfCr8PB-XK903GGNc").build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🟢 Bot avviato...")
    application.run_polling()

if __name__ == "__main__":
    main()
