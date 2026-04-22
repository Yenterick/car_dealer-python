from datetime import datetime
from babel.dates import format_datetime

# Gets a prefix with the actual time to log info
def getLogPrefix () -> str:
    now = datetime.now()
    timestamp = format_datetime(now, locale='en_US')
    return f"[car_dealer | {timestamp}] - "

# Logs info in the terminal
def log (message: str) -> None:
    print(f"{getLogPrefix()}{message}")