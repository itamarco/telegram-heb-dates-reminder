import logging
import os
import sys

import requests
import schedule
import time
from datetime import datetime, timedelta

HOST = os.environ.get("HOST")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")

echo_url = f"{HOST}/echo/{ADMIN_CHAT_ID}"
check_status_url = f"{HOST}/"
trigger_reminders_url = f"{HOST}/trigger-today-reminders"

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("Scheduler")


def trigger_reminders():
    response = requests.get(trigger_reminders_url)
    response_json = response.json()

    if response.status_code == 200:
        if response_json:
            logger.info("Status: %s", response_json["status"])
    else:
        raise Exception(f"Got unexpected response from server: {response_json['status']}")


schedule.every().day.at("09:00").do(trigger_reminders)

while True:
    schedule.run_pending()
    time.sleep(1)
