import os
import asyncio
from telegram.ext import ApplicationBuilder
from handlers import start_handler, message_handler

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(start_handler)
    app.add_handler(message_handler)

    print("🟢 PrimoGPT attivo in modalità polling...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
