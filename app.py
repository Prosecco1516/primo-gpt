"""
Flask application for the Telegram AI bot.
"""
import os
import logging
from flask import Flask, request, render_template, jsonify

import config
import bot

# Configure logging
logger = logging.getLogger(__name__)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

@app.route('/')
def index():
    """
    Render the home page.
    """
    return render_template('index.html', bot_name=config.BOT_NAME)

@app.route(config.WEBHOOK_PATH, methods=['POST'])
def webhook():
    """
    Handle webhook updates from Telegram.
    """
    return bot.handle_webhook()

@app.route('/setup', methods=['GET'])
def setup():
    """
    Set up the Telegram webhook.
    """
    webhook_url = config.WEBHOOK_URL + config.WEBHOOK_PATH
    result = bot.set_webhook(webhook_url)
    
    return jsonify({
        "success": result.get("ok", False),
        "description": result.get("description", "Unknown error"),
        "webhook_url": webhook_url
    })

@app.route('/remove', methods=['GET'])
def remove():
    """
    Remove the Telegram webhook.
    """
    result = bot.delete_webhook()
    
    return jsonify({
        "success": result.get("ok", False),
        "description": result.get("description", "Unknown error")
    })

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    """
    return jsonify({
        "status": "ok",
        "bot_token_configured": bool(config.TELEGRAM_BOT_TOKEN),
        "openai_api_key_configured": bool(config.OPENAI_API_KEY)
    })

@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 errors.
    """
    return render_template('index.html', bot_name=config.BOT_NAME), 404

@app.errorhandler(500)
def server_error(e):
    """
    Handle 500 errors.
    """
    logger.error(f"Server error: {e}")
    return render_template('index.html', bot_name=config.BOT_NAME, error=str(e)), 500
