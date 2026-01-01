import os
from typing import Optional
from dotenv import load_dotenv
from telethon import TelegramClient
from .logger import setup_logger

# Configure logging
logger = setup_logger(__name__)

# Load environment variables
load_dotenv()

# Constants
DEFAULT_TARGET_BOT = '@your_target_bot_username'
DEFAULT_SESSION_NAME = 'anon'

class TelegramBot:
    """
    A utility class to handle Telegram client creation and configuration.
    """
    def __init__(self):
        self.api_id = os.getenv('API_ID')
        self.api_hash = os.getenv('API_HASH')
        self.target_bot = os.getenv('TARGET_BOT_USERNAME', DEFAULT_TARGET_BOT)
        
        self._validate_credentials()

    def _validate_credentials(self):
        """Validates that API credentials are present and correct."""
        if not self.api_id or not self.api_hash:
            error_msg = "API_ID and API_HASH must be set in the .env file"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            self.api_id = int(self.api_id)
        except ValueError:
            error_msg = "API_ID must be an integer"
            logger.error(error_msg)
            raise ValueError(error_msg)

    def get_client(self, session_name: str = DEFAULT_SESSION_NAME) -> TelegramClient:
        """
        Creates and returns a TelegramClient instance.
        
        Args:
            session_name (str): The session name to use. Defaults to 'anon'.
            
        Returns:
            TelegramClient: The configured Telegram client.
        """
        return TelegramClient(session_name, self.api_id, self.api_hash)

    def get_target_bot(self) -> str:
        """
        Returns the target bot username.
        
        Returns:
            str: The target bot username.
        """
        return self.target_bot

# Convenience standalone functions to maintain backward compatibility
def get_client() -> TelegramClient:
    """
    Creates and returns a TelegramClient instance using credentials from .env
    """
    bot = TelegramBot()
    return bot.get_client()

def get_target_bot() -> str:
    """
    Returns the target bot username from .env or default
    """
    bot = TelegramBot()
    return bot.get_target_bot()
