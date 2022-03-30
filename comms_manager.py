import pymsteams
from smtplib import SMTP
import os
from dotenv import load_dotenv
from decorators import log_decorator

load_dotenv("_env/.env")
teams_webhook = os.getenv("TEAMS_WEBHOOK")


@log_decorator
def send_notification(date: str) -> None:
    """
    Function that sends notification to MS Teams channel

    :param date: date of summary report
    """
    message = pymsteams.connectorcard(teams_webhook)
    message.text(f"Summary report za den {date} je aktuální na dropboxu.")
    message.addLinkButton(buttontext="Soubory jsou zde.",
                          buttonurl="https://www.dropbox.com/sh/o72dhu4mtjhy3ee/AABnl5lA0qeAcPuq4lOJTm-ya?dl=0")
    message.send()

