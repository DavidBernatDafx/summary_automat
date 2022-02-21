import os
import shutil
from decorators import log_decorator
from pathlib import Path, PurePath
import time
import datetime as dt
from dotenv import load_dotenv

load_dotenv("_env/.env")
program_path = os.getenv("PROGRAM_PATH")
summary_path = os.getenv("SUMMARY_PATH")

# cwd = os.getcwd()
# source_path = Path("summary")
# destination_path = Path("summary_source")
cz_destination_files = ["DE01_Policies.xlsx", "DE02_Leads.xlsx", "S26_TimeToCall_CZ.xlsx", "DE01_Policies_all.xlsx",
                        "CM08_Rider_Upgrade_CZ.xlsx"]
sk_destination_files = ["DE01_Policies_SK.xlsx", "DE02_Leads_SK.xlsx", "S26_TimeToCall_SK.xlsx",
                        "DE01_Policies_all_SK.xlsx", "CM08_Rider_Upgrade_SK.xlsx"]
summary_file = "SummaryReport.xlsm"


class FileManager:

    def __init__(self, src_file: str, dest_file: str):
        self.source = f"{program_path}/data/{src_file}"
        print(self.source)
        self.renamed_source = f"{program_path}/data/{dest_file}"
        print(self.renamed_source)
        self.destination = f"{summary_path}/{dest_file}"
        self.rename_file()
        self.move_file()

    @log_decorator
    def rename_file(self):
        while True:
            if os.path.exists(self.source):
                print("file already saved")
                break
            else:
                time.sleep(1)
                print("waiting for saved file")
        return shutil.move(src=self.source, dst=self.renamed_source)

    @log_decorator
    def move_file(self):
        return shutil.move(src=self.renamed_source, dst=self.destination)


@log_decorator
def check_files(files: list):
    time_limit = dt.datetime.now() - dt.timedelta(minutes=5)
    print(time_limit)
    passed = None
    for file in files:
        modified_timestamp = os.path.getmtime(f"{summary_path}/{file}")
        modified_datetime = dt.datetime.fromtimestamp(modified_timestamp)
        print(modified_datetime)
        if modified_datetime < time_limit:
            passed = False
            break
        else:
            passed = True
    return passed



