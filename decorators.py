import datetime as dt
import sys
from time import sleep, time
import threading
import logging
from logging_manager import Logger

sys.stdout = Logger()


def log_decorator(func):
    """
    Decorator function prints actual running function/method name before
    and finished after decorated function/method was processed

    param func: decorated function
    return: wrapper function
    """
    def wrapper(*args, **kwargs):
        start = time()
        func_name = func.__name__
        print(f"Running: {func_name}")
        arg_count = func.__code__.co_argcount
        arg_names = func.__code__.co_varnames[:arg_count]
        zipped_args = zip(arg_names, args[:len(arg_names)])
        print(end="Parameters: ")
        print((", ".join("%s= %r" % entry for entry in zipped_args)), end=", ")
        print(f"args= {list(args[arg_count:])}", end=", ")
        print(f"kwargs= {kwargs}")

        with WaitingAnimation():
            result = func(*args, **kwargs)

        end = time()
        duration = end - start
        str_duration = round(duration, 3)

        print(f"Finished: OK in {str_duration} seconds.\n")
        return result
    return wrapper


class WaitingAnimation(threading.Thread):

    def __init__(self):
        super().__init__()
        self.daemon = True
        self.finished = False
        self.message = "Waiting"
        self.n_dots = 0
        self.to_delete = len(self.message) + self.n_dots

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def run(self):
        print(end=self.message)
        while not self.finished:

            if self.n_dots == 3:
                self.n_dots = 0
                print(end="\b\b\b", flush=True)

                # self.to_delete = len(self.message) + n_dots
                sleep(0.5)

            else:
                self.n_dots += 1
                print(end=".", flush=True)

                # self.to_delete = len(self.message) + n_dots
                sleep(0.5)

    def stop(self):
        self.to_delete = len(self.message) + self.n_dots
        self.finished = True
        for _ in range(self.to_delete):
            print(end="\b", flush=True)


