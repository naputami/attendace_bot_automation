import os
from datetime import datetime, date
from typing import Optional, Tuple, List
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource
from dotenv import load_dotenv
from .logger import setup_logger

# Configure logging
logger = setup_logger(__name__)

# Load environment variables
load_dotenv()

# Constants
CREDENTIALS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DEFAULT_CALENDAR_ID = 'en.indonesian#holiday@group.v.calendar.google.com'

class HolidayChecker:
    """
    A reusable utility class to check for public holidays using Google Calendar API.
    """
    
    def __init__(self, credentials_file: str = CREDENTIALS_FILE, calendar_id: str = DEFAULT_CALENDAR_ID):
        self.credentials_file = credentials_file
        self.calendar_id = calendar_id
        self._service: Optional[Resource] = None

    def _get_service(self) -> Optional[Resource]:
        """Authenticates and returns the Google Calendar service, caching it."""
        if self._service:
            return self._service

        if not os.path.exists(self.credentials_file):
            logger.error(f"Credentials file '{self.credentials_file}' not found.")
            return None
        
        try:
            credentials = Credentials.from_service_account_file(
                self.credentials_file, scopes=SCOPES
            )
            self._service = build('calendar', 'v3', credentials=credentials)
            return self._service
        except Exception as e:
            logger.error(f"Error authenticating with Google Calendar API: {e}")
            return None

    def is_holiday(self, check_date: date) -> Tuple[bool, Optional[str]]:
        """
        Checks if a specific date is a public holiday.
        
        Args:
            check_date (date): The date object to check.
            
        Returns:
            Tuple[bool, Optional[str]]: (True/False, Holiday Name or None)
        """
        service = self._get_service()
        if not service:
            return False, "Service Error"

        date_str = check_date.strftime('%Y-%m-%d')
        
        # Query for the specific day (full 24 hours UTC to cover all timezones/all-day events)
        time_min = f"{date_str}T00:00:00Z"
        time_max = f"{date_str}T23:59:59Z"

        try:
            events_result = service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])

            for event in events:
                # Check date match. All-day events usually have 'start': {'date': 'YYYY-MM-DD'}
                start = event['start'].get('date') or event['start'].get('dateTime')
                
                # Simple string match for date is usually sufficient for all-day events
                if start and start.startswith(date_str):
                    return True, event['summary']
            
            return False, None

        except Exception as e:
            logger.error(f"API Error while checking holiday: {e}")
            return False, "API Error"


# Convenience standalone function
def is_today_holiday() -> Tuple[bool, Optional[str]]:
    """Check if today is a holiday using default settings."""
    checker = HolidayChecker()
    return checker.is_holiday(datetime.now().date())
