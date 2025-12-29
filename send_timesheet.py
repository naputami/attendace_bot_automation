import asyncio
import gspread
import os
from dotenv import load_dotenv
from datetime import datetime
from google.oauth2.service_account import Credentials
from telegram_utils import get_client, get_target_bot


# --- Configuration ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

load_dotenv()

CREDENTIALS_FILE = 'credentials.json'
SPREADSHEET_NAME = os.getenv('SPREADSHEET_NAME')

# Column Names (must match exactly what's in the sheet)
COL_ACTUAL_DATE = os.getenv('COL_ACTUAL_DATE')
COL_PROJECT = os.getenv('COL_PROJECT')
COL_TASK = os.getenv('COL_TASK')
COL_EFF_HOURS = os.getenv('COL_EFF_HOURS')
WORKSHEET_TITLE = os.getenv('WORKSHEET_TITLE')

def get_sheet_client():
    """Authenticates and returns the gspread client."""
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"'{CREDENTIALS_FILE}' not found. Please place your Service Account JSON here.")
    
    credentials = Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    return gspread.authorize(credentials)

def get_todays_tasks():
    """Fetches tasks from the spreadsheet where actual_date is today."""
    try:
        gc = get_sheet_client()
        print(f"Opening spreadsheet: '{SPREADSHEET_NAME}'...")
        sh = gc.open(SPREADSHEET_NAME)
        worksheet = sh.worksheet(WORKSHEET_TITLE)
        
        print("Fetching all records...")
        all_records = worksheet.get_all_records()
        
        # Determine today's date format
        # Adjust this format if your spreadsheet uses something else (e.g., "%d/%m/%Y")
        today_str = datetime.now().strftime("%d-%m-%Y")
        print(f"Looking for tasks with date: {today_str}")
        
        todays_tasks = []
        for row in all_records:
            # We convert to string and strip whitespace to be safe
            row_date = str(row.get(COL_ACTUAL_DATE, '')).strip()
            
            # Basic date comparison
            # If your sheet has time included or different formats, you might need more robust parsing
            if row_date == today_str:
                todays_tasks.append(row)
                
        return todays_tasks, today_str

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet '{SPREADSHEET_NAME}' not found.")
        return [], None
    except gspread.exceptions.WorksheetNotFound:
        print(f"Error: Worksheet '{WORKSHEET_TITLE}' not found in spreadsheet '{SPREADSHEET_NAME}'.")
        return [], None
    except Exception as e:
        print(f"Error fetching sheet data: {e}")
        return [], None

async def send_telegram_messages(tasks):
    """Sends the formatted messages to Telegram."""
    if not tasks:
        print("No tasks to send.")
        return

    client = get_client()
    target_bot = get_target_bot()
    
    print("Connecting to Telegram...")
    await client.start()
    
    try:
        for task in tasks:
            # Format: /ts {project}:{task}:{eff_hours}:{actual_date}
            project = task.get(COL_PROJECT, '')
            task_desc = task.get(COL_TASK, '')
            eff_hours = task.get(COL_EFF_HOURS, '')
            actual_date = task.get(COL_ACTUAL_DATE, '')
            
            message_text = f"/ts {project}:{task_desc}:{eff_hours}:{actual_date}"
            
            print(f"Sending: {message_text}")
            await client.send_message(target_bot, message_text)
            # Small delay to avoid hitting rate limits if many messages
            await asyncio.sleep(3)
            
        print("All messages sent successfully!")
        
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
    finally:
        await client.disconnect()

async def main():
    tasks, today_str = get_todays_tasks()
    
    if tasks:
        print(f"Found {len(tasks)} tasks for today ({today_str}). Sending to Telegram...")
        await send_telegram_messages(tasks)
    else:
        print(f"No tasks found for today ({today_str}). Skipping Telegram.")

if __name__ == '__main__':
    asyncio.run(main())
