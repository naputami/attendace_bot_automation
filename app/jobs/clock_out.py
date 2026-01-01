import asyncio
from app.utils.telegram import get_client, get_target_bot
from app.utils.holiday import is_today_holiday
from app.utils.logger import setup_logger

# Configure logging
logger = setup_logger(__name__)

async def main():
    # Check for holiday
    is_holiday, holiday_name = is_today_holiday()
    if is_holiday:
        logger.info(f"Today is {holiday_name}. Skipping Clock Out.")
        return

    client = get_client()
    target_bot = get_target_bot()
    message_text = '/clock_out'

    logger.info("Connecting to Telegram...")
    await client.start()
    
    logger.info(f"Sending '{message_text}' to {target_bot}...")
    try:
        await client.send_message(target_bot, message_text)
        logger.info("Clock Out message sent successfully!")
    except Exception as e:
        logger.error(f"Error sending message: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
