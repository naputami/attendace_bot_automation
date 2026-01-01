#!/bin/bash
cd /home/ubuntu/attendace_bot_automation
source .venv/bin/activate
python -m app.jobs.send_timesheet
