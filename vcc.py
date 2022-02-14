import requests
from decorators import log_decorator
import os
from dotenv import load_dotenv
from pprint import pprint
import math

load_dotenv("_env/.env")
API_KEY = os.getenv("vcc_api_key")
ACCOUNT = os.getenv("vcc_account")


class VccCdr:

    def __init__(self, project_id: int, year: str, month: str):     # project id's: 15, 32, 39, 41
        self.project_id = project_id
        self.year = year            # actual year
        self.month = month          # actual month
        self.cdr_data = None
        self.cdr_count = None
        self.get_cdr_report()

    @log_decorator
    def get_cdr_report(self):
        url = f"https://{ACCOUNT}:{API_KEY}@{ACCOUNT}.asp.virtual-call-center.eu/v2/cdrs/{self.year}/{self.month}"
        options = {"projectid": self.project_id,
                   "num": 1000,
                   }

        with requests.get(url, options) as response:
            response.raise_for_status()
            data = response.json()
        self.cdr_data = data["response"]["rows"]
        self.cdr_count = int(data["response"]["totalCount"])

        # added for loop here to iterate from records offset starting at 500, 1000 depending on count of iterations
        if self.cdr_count > 500:
            loop_count = math.floor(self.cdr_count / 500)

            for i in range(loop_count):
                new_options = {"projectid": self.project_id,
                               "num": 1000,
                               "start": (i + 1) * 500,
                               }
                with requests.get(url, new_options) as next_response:
                    next_response.raise_for_status()
                    next_data = next_response.json()
                    next_cdr_data = next_data["response"]["rows"]

                for record in next_cdr_data:
                    self.cdr_data.append(record)


class VccUserState:

    def __init__(self, from_date: str, to_date: str):
        self.from_date = from_date
        self.to_date = to_date
        self.log_data = None
        self.log_count = None
        self.get_user_state_report()

    def get_user_state_report(self):
        url = f"https://{ACCOUNT}:{API_KEY}@{ACCOUNT}.asp.virtual-call-center.eu/v2/statistics/userstate"
        options = {
            "from": self.from_date,
            "to": self.to_date,
            "direction": "ASC"
        }
        with requests.get(url, options) as response:
            response.raise_for_status()
            data = response.json()
        self.log_data = data["response"]


