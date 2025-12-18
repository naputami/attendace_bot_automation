import os
from dotenv import load_dotenv
from telethon import TelegramClient

# Load environment variables
load_dotenv()

def get_client():
    """
    Creates and returns a TelegramClient instance using credentials from .env
    """
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')

    if not api_id or not api_hash:
        raise ValueError("API_ID and API_HASH must be set in the .env file")

    try:
        api_id = int(api_id)
    except ValueError:
        raise ValueError("API_ID must be an integer")

    # 'anon' session name can be reused across scripts
    return TelegramClient('anon', api_id, api_hash)

def get_target_bot():
    """
    Returns the target bot username from .env or default
    """
    return os.getenv('TARGET_BOT_USERNAME', '@your_target_bot_username')
