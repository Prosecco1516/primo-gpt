"""
Configuration file for the Telegram AI bot application.
"""
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Telegram Bot Token - Must be set in environment variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    logger.error("No TELEGRAM_BOT_TOKEN found in environment variables!")

# OpenAI API Key - Must be set in environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("No OPENAI_API_KEY found in environment variables!")

# Webhook settings
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")
WEBHOOK_PATH = f"/webhook/{TELEGRAM_BOT_TOKEN}"

# Flask server settings
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000

# OpenAI settings
AI_MODEL = "gpt-4o"  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
                     # do not change this unless explicitly requested by the user
MAX_TOKENS = 500
TEMPERATURE = 0.7

# Bot settings
BOT_NAME = "AI Assistant"
HELP_TEXT = """
I'm your AI assistant! Here's what I can do:

/start - Start a conversation with me
/help - Show this help message
/about - Learn more about me
/reset - Reset our conversation history

You can also just send me a message and I'll respond with AI-generated content!
"""

ABOUT_TEXT = """
I'm an AI-powered Telegram bot created to assist you. 
I use OpenAI's GPT-4o model to generate responses.
"""

# Conversation settings
MAX_CONVERSATION_LENGTH = 10  # Number of messages to keep in memory per user
