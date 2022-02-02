import os
from dotenv import load_dotenv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from decorators import log_decorator
from pprint import pprint

load_dotenv("_env/.env")
URL = os.getenv("url")
USERNAME = os.getenv("username")
CZ_PASSWORD = os.getenv("cz_pass")
SK_COMPASS = os.getenv("sk_pass")
DRIVER_PATH = os.getenv("driver_path")


class Browser:

    def __init__(self):
        self.service = Service(executable_path=DRIVER_PATH)
        self.options = webdriver.ChromeOptions()
        self.prefs = {"download.default_directory": "D:\\4life\data\\"}
        self.options.add_experimental_option("prefs", self.prefs)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.tabs = []

    @log_decorator
    def load_cz_compass(self, loc: str):
        url = f"{URL}{loc}"
        self.driver.get(url=url)

    @log_decorator
    def login_cz(self):
        time.sleep(1)
        user_inputs = self.driver.find_elements(by=By.TAG_NAME, value="input")
        username = user_inputs[0]
        password = user_inputs[1]
        submit_button = self.driver.find_element(by=By.ID, value="btnLogin")

        username.send_keys(USERNAME)
        password.send_keys(CZ_PASSWORD)
        submit_button.click()

    @log_decorator
    def open_tabs(self, tab_count: int):
        for i in range(tab_count):
            self.driver.execute_script("window.open()")
            self.driver.switch_to.window(self.driver.window_handles[i + 1])

    @log_decorator
    def get_tab_objects(self):
        tabs_list = [window for window in self.driver.window_handles[1::]]
        self.tabs = tabs_list
        pprint(self.tabs)

    @log_decorator
    def load_report_urls(self, data):
        for i in range(len(data)):
            self.driver.switch_to.window(data[i]["tab"])
            self.driver.get(data[i]["path"])
            time.sleep(1)
