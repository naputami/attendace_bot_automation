import asyncio
from telegram_utils import get_client, get_target_bot

async def main():
    client = get_client()
    target_bot = get_target_bot()
    message_text = '/clock_out'

    print("Connecting to Telegram...")
    await client.start()
    
    print(f"Sending '{message_text}' to {target_bot}...")
    try:
        await client.send_message(target_bot, message_text)
        print("Clock Out message sent successfully!")
    except Exception as e:
        print(f"Error sending message: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
