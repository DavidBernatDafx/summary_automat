import os
import shutil
from decorators import log_decorator
from pathlib import Path, PurePath
import time

cwd = os.getcwd()
source_path = Path("summary")
destination_path = Path("summary_source")


class FileManager:

    def __init__(self, src_file: str, dest_file: str):
        self.source = f"D:/4life/data/{src_file}"
        print(self.source)
        self.renamed_source = f"D:/4life/data/{dest_file}"
        print(self.renamed_source)
        self.destination = f"D:/4life/summary_source/{dest_file}"
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
