# Telegram Attendance & Timesheet Automation

This project automates the process of clocking in, clocking out, and submitting daily timesheets to a specific Telegram bot. It integrates with Google Sheets to fetch daily tasks and reports them automatically.

## Features

- **Automated Clock In/Out**: Send `/clock_in` and `/clock_out` commands to a target Telegram bot via scripts.
- **Google Sheets Integration**: Fetches daily tasks from a specified Google Spreadsheet.
- **Timesheet Submission**: Formats and sends task details (Project, Task Description, Effective Hours) to the Telegram bot.
- **Configurable**: Uses `.env` for easy configuration of API credentials and sheet settings.

## Prerequisites

- Python 3.7+
- A Telegram account (to create the API application).
- A Google Cloud Service Account (for accessing Google Sheets).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd virgo_auto
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
2.  Download the JSON key file.
3.  Rename it to `credentials.json` and place it in the project root directory.
4.  **Important:** Share your Google Spreadsheet with the `client_email` found in `credentials.json`.

## Usage

### Run Manually

*   **Clock In:**
    ```bash
    python clock_in.py
    ```

*   **Clock Out:**
    ```bash
    python clock_out.py
    ```

*   **Send Timesheet:**
    fetches tasks for the *current date* from the spreadsheet and sends them.
    ```bash
    python send_timesheet.py
    ```

### First Run
When running the scripts for the first time, Telethon might ask you to login with your phone number and enter the code sent to your Telegram app. This creates a session file (`anon.session`) so subsequent runs won't require manual login.

### Automation (Shell Scripts)
The `scripts/` directory contains bash scripts (`clock_in.sh`, `clock_out.sh`, `send_timesheet.sh`) that can be used with `cron` or other schedulers.

**Note:** You may need to update the paths in these scripts to match your deployment environment.

Example `scripts/clock_in.sh`:
```bash
#!/bin/bash
cd /path/to/your/project
source .venv/bin/activate
python clock_in.py
```

## Project Structure

- `clock_in.py`: Script to send the clock-in command.
- `clock_out.py`: Script to send the clock-out command.
- `send_timesheet.py`: Main logic for reading sheets and sending reports.
- `telegram_utils.py`: Helper functions for Telegram client.
- `requirements.txt`: Python dependencies.
- `scripts/`: Shell scripts for automation.
