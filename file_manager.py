import os
import shutil
import sys

from decorators import log_decorator
from pathlib import Path, PurePath
import time
import datetime as dt
from dotenv import load_dotenv

# loading environment variables
load_dotenv("_env/.env")
summary_path = os.getenv("SUMMARY_PATH")
dropbox_path = os.getenv("DROPBOX_PATH")

cwd = os.getcwd()

cz_destination_files = ["DE01_Policies.xlsx", "DE02_Leads.xlsx", "S26_TimeToCall_CZ.xlsx", "DE01_Policies_all.xlsx",
                        "CM08_Rider_Upgrade_CZ.xlsx"]
sk_destination_files = ["DE01_Policies_SK.xlsx", "DE02_Leads_SK.xlsx", "S26_TimeToCall_SK.xlsx",
                        "DE01_Policies_all_SK.xlsx", "CM08_Rider_Upgrade_SK.xlsx"]
summary_file = "SummaryReport.xlsm"


class FileManager:
    """
    Class that represents file manipulations

    Attributes
    ----------
    source : str
        path to downloaded file in data folder
    renamed_source : str
        path to renamed file in data folder
    destination : str
        path for renamed file in summary folder

    Methods
    -------
    rename_file()
        renames downloaded file to target name in data folder
    move_file()
        move renamed file from data folder to summary folder
    """

    def __init__(self, src_file: str, dest_file: str):
        # self.source = f"{program_path}/data/{src_file}"
        # self.renamed_source = f"{program_path}/data/{dest_file}"
        # self.destination = f"{summary_path}/{dest_file}"
        self.source = os.path.join(cwd, "data", src_file)
        self.renamed_source = os.path.join(cwd, "data", dest_file)
        self.destination = os.path.join(summary_path, dest_file)
        self.dest_file = dest_file
        self.rename_file()
        self.move_file()

    def __repr__(self):
        return f"<{self.dest_file} File object>"

    @log_decorator
    def rename_file(self) -> None:
        """
        Method that renames downloaded file to target filename

        return: None
        """
        while True:
            if os.path.exists(self.source):
                break
            else:
                time.sleep(1)
        return shutil.move(src=self.source, dst=self.renamed_source)

    @log_decorator
    def move_file(self) -> None:
        """
        Method that moves file from data folder to summary folder

        return: None
        """
        return shutil.move(src=self.renamed_source, dst=self.destination)


@log_decorator
def check_files(files: list) -> bool:
    """
    Function that checks date modified for all files in files list and returns True,
    if files are newer than 5 minutes

    param list files: list of files for date modified check
    return: bool
    """
    time_limit = dt.datetime.now() - dt.timedelta(minutes=5)
    passed = None
    for file in files:
        modified_timestamp = os.path.getmtime(f"{summary_path}/{file}")
        modified_datetime = dt.datetime.fromtimestamp(modified_timestamp)
        if modified_datetime < time_limit:
            passed = False
            break
        else:
            passed = True
    return passed


@log_decorator
def copy_to_dropbox(src: str, dest: str) -> None:
    """
    Function that copies all files from local summary folder to dropbox summary folder

    param str src: path local summary folder
    param src dest: path to dropbox summary folder
    return: None
    """
    all_files = os.listdir(src)
    for file in all_files:
        full_file_path = os.path.join(src, file)
        if os.path.isfile(full_file_path):
            shutil.copy(full_file_path, dest)
