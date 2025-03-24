"""
Utility functions for the Telegram AI bot.
"""
import logging
from typing import Dict, List, Any, Optional
import json
import os

# Configure logging
logger = logging.getLogger(__name__)

# Store user conversations in memory
# In a production environment, this would be replaced with a database
user_conversations: Dict[int, List[Dict[str, str]]] = {}

def get_user_conversation(user_id: int) -> List[Dict[str, str]]:
    """
    Get the conversation history for a user.
    
    Args:
        user_id: The Telegram user ID
        
    Returns:
        List of conversation messages
    """
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    return user_conversations[user_id]

def add_message_to_conversation(user_id: int, role: str, content: str) -> None:
    """
    Add a message to the user's conversation history.
    
    Args:
        user_id: The Telegram user ID
        role: The role of the message sender ("user" or "assistant")
        content: The message content
    """
    from config import MAX_CONVERSATION_LENGTH
    
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    
    user_conversations[user_id].append({
        "role": role,
        "content": content
    })
    
    # Limit conversation length
    if len(user_conversations[user_id]) > MAX_CONVERSATION_LENGTH:
        user_conversations[user_id] = user_conversations[user_id][-MAX_CONVERSATION_LENGTH:]

def reset_conversation(user_id: int) -> None:
    """
    Reset a user's conversation history.
    
    Args:
        user_id: The Telegram user ID
    """
    user_conversations[user_id] = []

def log_interaction(user_id: int, user_message: str, bot_response: str) -> None:
    """
    Log user-bot interactions for monitoring and debugging.
    
    Args:
        user_id: The Telegram user ID
        user_message: The message from the user
        bot_response: The bot's response
    """
    logger.info(f"User {user_id} sent: {user_message}")
    logger.info(f"Bot responded: {bot_response}")
