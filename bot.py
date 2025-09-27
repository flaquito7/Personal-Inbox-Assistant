from dotenv import load_dotenv
import os
import time

load_dotenv()

from outlook import get_emails
from telegram import send
from filters import important

def main():
    while True:
        emails = get_emails()
        for email in emails:
            if important(email):
                folder_icon = "🗂️" if email.get('_folder') == 'Junk' else "📥"
                folder_text = f" [{email.get('_folder', 'Inbox')}]" if email.get('_folder') == 'Junk' else ""
                msg = f"{folder_icon} {email['subject']} from {email['from']['emailAddress']['address']}{folder_text}"
                send(msg)
        time.sleep(21600)  # wait 6 hours (6 * 60 * 60 = 21600 seconds)

if __name__ == "__main__":
    main()
    
