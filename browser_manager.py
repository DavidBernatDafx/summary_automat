import os
from dotenv import load_dotenv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from decorators import log_decorator
from pprint import pprint

load_dotenv("_env/.env")
url = os.getenv("URL")
username = os.getenv("USERNAME")
cz_password = os.getenv("CZ_PASS")
sk_password = os.getenv("SK_PASS")
driver_path = os.getenv("DRIVER_PATH")


class Browser:

    def __init__(self):
        self.service = Service(executable_path=driver_path)
        self.options = webdriver.ChromeOptions()
        self.prefs = {"download.default_directory": "D:\\summary_automat\data\\"}
        self.options.add_experimental_option("prefs", self.prefs)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.tabs = []

    @log_decorator
    def load_cz_compass(self, loc: str):
        cz_url = f"{url}{loc}"
        self.driver.get(url=cz_url)

    @log_decorator
    def load_sk_compass(self, loc: str):
        sk_url = f"{url}{loc}"
        self.driver.get(url=sk_url)

    @log_decorator
    def login_cz(self):
        time.sleep(1)
        user_inputs = self.driver.find_elements(by=By.TAG_NAME, value="input")
        compass_username = user_inputs[0]
        password = user_inputs[1]
        submit_button = self.driver.find_element(by=By.ID, value="btnLogin")

        compass_username.send_keys(username)
        password.send_keys(sk_password)
        submit_button.click()

    @log_decorator
    def login_sk(self):
        time.sleep(1)
        user_inputs = self.driver.find_elements(by=By.TAG_NAME, value="input")
        compass_username = user_inputs[0]
        password = user_inputs[1]
        submit_button = self.driver.find_element(by=By.ID, value="btnLogin")

        compass_username.send_keys(username)
        password.send_keys(sk_password)
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
