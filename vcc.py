import requests
from decorators import log_decorator
import os
from dotenv import load_dotenv

load_dotenv("_env/.env")
API_KEY = os.getenv("vcc_api_key")
ACCOUNT = os.getenv("vcc_account")


class VccCdr:

    def __init__(self, project_id: int, year: str, month: str):
        # self.url = f"https://{ACCOUNT}:{API_KEY}@{ACCOUNT}.asp.virtual-call-center.eu/v2/cdrs/{year}/{month}"
        self.project_id = project_id
        self.year = year
        self.month = month
        self.cdr_data = None
        self.get_cdr_report()

    @log_decorator
    def get_cdr_report(self):
        url = f"https://{ACCOUNT}:{API_KEY}@{ACCOUNT}.asp.virtual-call-center.eu/v2/cdrs/{self.year}/{self.month}"
        options = {"projectid": str(self.project_id),
                   "num": "5000"}

        with requests.get(url, options) as response:
            response.raise_for_status()
            data = response.json()
            self.cdr_data = data["response"]["rows"]

