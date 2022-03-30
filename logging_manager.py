import sys
from datetime import datetime


now = datetime.now()
str_now = now.strftime("%d_%m_%Y_%H_%M")


class Logger(object):

    def __init__(self):
        self.terminal = sys.stdout
        self.log = open(f"logs/log_{str_now}.txt", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()
