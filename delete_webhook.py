async def delete_webhook_if_exists(app):
    await app.bot.delete_webhook()
    print("✅ Webhook eliminato prima di avviare il polling.")
