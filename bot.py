"""
Telegram bot functionality and message handling.
"""
import logging
import json
from typing import Dict, Any, Optional

import requests
from flask import request, Response

import config
import ai
import utils

# Configure logging
logger = logging.getLogger(__name__)

def send_message(chat_id: int, text: str) -> Dict[str, Any]:
    """
    Send a message to a Telegram chat.
    
    Args:
        chat_id: The Telegram chat ID
        text: The message text
        
    Returns:
        The API response
    """
    api_url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(api_url, json=data)
        return response.json()
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        return {"ok": False, "description": str(e)}

def set_webhook(webhook_url: str) -> Dict[str, Any]:
    """
    Set the Telegram bot webhook.
    
    Args:
        webhook_url: The URL for Telegram to send updates to
        
    Returns:
        The API response
    """
    api_url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/setWebhook"
    data = {
        "url": webhook_url
    }
    
    try:
        response = requests.post(api_url, json=data)
        return response.json()
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")
        return {"ok": False, "description": str(e)}

def delete_webhook() -> Dict[str, Any]:
    """
    Delete the Telegram bot webhook.
    
    Returns:
        The API response
    """
    api_url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/deleteWebhook"
    
    try:
        response = requests.get(api_url)
        return response.json()
    except Exception as e:
        logger.error(f"Failed to delete webhook: {e}")
        return {"ok": False, "description": str(e)}

def handle_webhook() -> Response:
    """
    Handle a webhook update from Telegram.
    
    Returns:
        Flask response
    """
    try:
        # Parse the update
        update = request.get_json()
        logger.debug(f"Received update: {update}")
        
        # Process the update
        process_update(update)
        
        return Response("OK", status=200)
    
    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        return Response(f"Error: {e}", status=500)

def process_update(update: Dict[str, Any]) -> None:
    """
    Process a Telegram update.
    
    Args:
        update: The Telegram update object
    """
    # Check if the update contains a message
    if "message" not in update:
        logger.debug("Update doesn't contain a message")
        return
    
    message = update["message"]
    
    # Check if the message contains text
    if "text" not in message:
        logger.debug("Message doesn't contain text")
        return
    
    # Extract message data
    chat_id = message["chat"]["id"]
    user_id = message["from"]["id"]
    text = message["text"]
    
    # Handle commands
    if text.startswith("/"):
        handle_command(chat_id, user_id, text)
    else:
        handle_message(chat_id, user_id, text)

def handle_command(chat_id: int, user_id: int, text: str) -> None:
    """
    Handle a command from a user.
    
    Args:
        chat_id: The Telegram chat ID
        user_id: The Telegram user ID
        text: The command text
    """
    # Extract the command and parameters
    parts = text.split(None, 1)
    command = parts[0].lower()
    
    # Process the command
    if command == "/start":
        response = f"👋 Hello! {config.HELP_TEXT}"
        send_message(chat_id, response)
        
    elif command == "/help":
        send_message(chat_id, config.HELP_TEXT)
        
    elif command == "/about":
        send_message(chat_id, config.ABOUT_TEXT)
        
    elif command == "/reset":
        utils.reset_conversation(user_id)
        send_message(chat_id, "🔄 I've reset our conversation history. Let's start fresh!")
        
    else:
        # Handle unknown command
        send_message(chat_id, "I don't recognize that command. Try /help to see what I can do.")

def handle_message(chat_id: int, user_id: int, text: str) -> None:
    """
    Handle a regular message from a user.
    
    Args:
        chat_id: The Telegram chat ID
        user_id: The Telegram user ID
        text: The message text
    """
    try:
        # Let the user know we're processing
        send_message(chat_id, "⏳ Thinking...")
        
        # Add the user message to the conversation history
        utils.add_message_to_conversation(user_id, "user", text)
        
        # Get the conversation history
        conversation_history = utils.get_user_conversation(user_id)
        
        # Generate an AI response
        response = ai.generate_response(text, conversation_history)
        
        # Add the AI response to the conversation history
        utils.add_message_to_conversation(user_id, "assistant", response)
        
        # Send the response
        send_message(chat_id, response)
        
        # Log the interaction
        utils.log_interaction(user_id, text, response)
        
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        send_message(chat_id, "I'm having some technical difficulties. Please try again later.")
