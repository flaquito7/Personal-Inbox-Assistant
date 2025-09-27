from dotenv import load_dotenv
import os
import time
from outlook import get_emails
from telegram import send
from filters import important

load_dotenv()

def main():
    while True:
        emails = get_emails()
        for email in emails:
            if important(email):
                msg = f"📧 {email['subject']} from {email['from']['emailAddress']['address']}"
                send(msg)
        time.sleep(300)  # wait 5 minutes

if __name__ == "__main__":
    main()
