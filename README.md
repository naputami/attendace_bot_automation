# Telegram Attendance & Timesheet Automation

This project automates the process of clocking in, clocking out, and submitting daily timesheets to a specific Telegram bot. It integrates with Google Sheets to fetch daily tasks and intelligently skips operations on public holidays.

## Features

- **Automated Clock In/Out**: Send `/clock_in` and `/clock_out` commands to a target Telegram bot.
- **Google Sheets Integration**: Fetches daily tasks from a specified Google Spreadsheet.
- **Timesheet Submission**: Formats and sends task details (Project, Task Description, Effective Hours) to the Telegram bot.
- **Holiday Awareness**: Automatically checks for Indonesian public holidays (via Google Calendar) and skips actions if today is a holiday.
- **Robust Logging**: Uses a centralized logging system for better debugging and monitoring.
- **Modular Design**: Code is organized into jobs and utilities for better maintainability.

## Prerequisites

- Python 3.7+
- A Telegram account (to create the API application).
- A Google Cloud Service Account with:
  - **Google Sheets API** enabled.
  - **Google Calendar API** enabled.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd attendace_bot_automation
    ```

2.  **Create and activate a virtual environment (optional but recommended):**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/macOS
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

### 1. Environment Variables (.env)
Create a `.env` file in the root directory and add the following configuration:

```ini
# Telegram API Credentials
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
TARGET_BOT_USERNAME=@your_target_bot_username

# Google Sheets Configuration
SPREADSHEET_NAME=Your Spreadsheet Name
WORKSHEET_TITLE=Sheet1

# Spreadsheet Column Headers (Must match exactly)
COL_ACTUAL_DATE=Actual Date
COL_PROJECT=Project
COL_TASK=Task
COL_EFF_HOURS=Effective Hours
```

*   **Telegram API:** Get your `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org).
*   **Google Sheets:** Ensure the `SPREADSHEET_NAME` matches your file in Google Drive.

### 2. Google Credentials
1.  Create a Service Account in Google Cloud Console.
2.  Enable **Google Sheets API** and **Google Calendar API** for this project.
3.  Download the JSON key file.
4.  Rename it to `credentials.json` and place it in the project root directory.
5.  **Important:** Share your Google Spreadsheet with the `client_email` found in `credentials.json`.

## Usage

Run the scripts as Python modules from the project root directory.

### Run Manually

*   **Clock In:**
    ```bash
    python -m app.jobs.clock_in
    ```

*   **Clock Out:**
    ```bash
    python -m app.jobs.clock_out
    ```

*   **Send Timesheet:**
    Fetches tasks for the *current date* from the spreadsheet and sends them.
    ```bash
    python -m app.jobs.send_timesheet
    ```

### First Run
When running the scripts for the first time, Telethon might ask you to login with your phone number and enter the code sent to your Telegram app. This creates a session file (`anon.session`) so subsequent runs won't require manual login.

### Automation (Shell Scripts)
The `shell_scripts/` directory contains bash scripts that are ready to be used with `cron` or other schedulers.

**Note:** You may need to update the absolute paths in these scripts to match your deployment environment.

Example `shell_scripts/clock_in.sh`:
```bash
#!/bin/bash
cd /path/to/your/project
source .venv/bin/activate
python -m app.jobs.clock_in
```

## Project Structure

```
attendace_bot_automation/
├── app/
│   ├── jobs/               # Main executable scripts
│   │   ├── clock_in.py
│   │   ├── clock_out.py
│   │   └── send_timesheet.py
│   └── utils/              # Shared utilities
│       ├── holiday.py      # Holiday checking logic
│       ├── logger.py       # Logging configuration
│       └── telegram.py     # Telegram client helpers
├── shell_scripts/          # Bash scripts for cron jobs
├── .env                    # Configuration variables
├── credentials.json        # Google Service Account Key (ignored in git)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```
