import logging
import os
import requests
import json
from datetime import datetime, timedelta

DOMAIN = os.environ.get("DOMAIN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
echo_url = f"{DOMAIN}/echo/{ADMIN_CHAT_ID}"
check_status_url = f"{DOMAIN}/"
trigger_reminders = f"{DOMAIN}/trigger-today-reminders"

logger = logging.getLogger("cron-job")


def is_near_hour(hour: int):
    now = datetime.now()

    target_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)

    # Define a time window of 2 minutes before and after input hour
    time_window_start = target_time - timedelta(minutes=2)
    time_window_end = target_time + timedelta(minutes=2)

    # Check if the current time is within the time window
    if time_window_start <= now <= time_window_end:
        return True
    else:
        return False


try:
    # if on 6:00 UTC time (9 in Israel) trigger reminders
    request_url = trigger_reminders if is_near_hour(6) else check_status_url
    response = requests.get(request_url)
    response_json = response.json()

    if response.status_code == 200 and response_json.get("status") == "ok":
        logger.info("Status:", response_json["status"])
    else:
        logger.error("Unexpected response:", response_json.get("status"))

except requests.RequestException as e:
    logger.exception("cron job failed")
