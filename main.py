# main.py
import asyncio
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from bot.handlers import start_command, handle_message

async def main():
    application = ApplicationBuilder().token("8108284075:AAHs2urWXlt0sGzXG2EfCr8PB-XK903GGNc").build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🟢 Bot avviato...")
    await application.run_polling(close_loop=False)

if __name__ == "__main__":
    asyncio.run(main())
