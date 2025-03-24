"""
OpenAI integration for the Telegram bot.
"""
import json
import logging
from typing import List, Dict, Any

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

import config

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai = OpenAI(api_key=config.OPENAI_API_KEY)

def generate_response(user_input: str, conversation_history: List[Dict[str, str]] = None) -> str:
    """
    Generate an AI response based on user input and conversation history.
    
    Args:
        user_input: The message from the user
        conversation_history: Previous messages in the conversation
        
    Returns:
        str: The AI-generated response
    """
    try:
        # Prepare the messages for the API
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": (
                "You are a helpful, friendly, and conversational assistant in a Telegram bot. "
                "Provide concise, helpful responses. If you don't know something, admit it. "
                "Don't fabricate information. Be polite and respectful."
            )}
        ]
        
        # Add conversation history if available
        if conversation_history:
            for message in conversation_history:
                messages.append({"role": message["role"], "content": message["content"]})
        
        # Add the current user message
        messages.append({"role": "user", "content": user_input})
        
        # Generate the response
        response = openai.chat.completions.create(
            model=config.AI_MODEL,
            messages=messages,
            max_tokens=config.MAX_TOKENS,
            temperature=config.TEMPERATURE,
        )
        
        # Extract and return the response text
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return "I'm having trouble connecting to my AI brain right now. Please try again later."
