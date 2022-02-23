import os
from dotenv import load_dotenv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from decorators import log_decorator
from pprint import pprint

# loading environment variables
load_dotenv("_env/.env")
url = os.getenv("URL")
username = os.getenv("USERNAME")
cz_password = os.getenv("CZ_PASS")
sk_password = os.getenv("SK_PASS")
driver_path = os.getenv("DRIVER_PATH")


class Browser:
    """
    A class that represents chrome driver to manipulate with browser

    Attributes
    ----------
    None

    Methods
    -------
    load_cz_compass(loc: str)
        load cz compass webpage in chrome
    load_sk_compass(loc: str)
        load sk compass webpage in chrome
    login_cz()
        log in to cz compass
    login_sk()
        log in to sk compass
    open_tabs(tab_count: int)
        open passed count of new Chrome tabs
    get_tab_objects()
        populates self.tabs list with Chrome tab objects
    load_report_urls(data: dict)
        load report urls in respective Chrome tabs
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """
        self.service = Service(executable_path=driver_path)
        self.options = webdriver.ChromeOptions()
        self.prefs = {"download.default_directory": "D:\\summary_automat\data\\"}
        # needs to be changed to actual project folder/data
        self.options.add_experimental_option("prefs", self.prefs)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.tabs = []

    @log_decorator
    def load_cz_compass(self, loc: str) -> webdriver.Chrome:
        """ Method that loads cz compass webpage with selenium driver in Chrome window

        :param str loc: string representing end of the url after last dot e.g. "cz"
        :return webdriver.Chrome
        """
        cz_url = f"{url}{loc}"
        self.driver.get(url=cz_url)

    @log_decorator
    def load_sk_compass(self, loc: str) -> webdriver.Chrome:
        """ Method that loads cz compass webpage with selenium driver in Chrome window

        :param str loc: string representing end of the url after last dot e.g. "sk"
        :return webdriver.Chrome
        """
        sk_url = f"{url}{loc}"
        self.driver.get(url=sk_url)

    @log_decorator
    def login_cz(self) -> None:
        """
        Method that log in user to cz compass
        log in detail are passed automatically from .env file

        :return None
        """
        time.sleep(1)
        user_inputs = self.driver.find_elements(by=By.TAG_NAME, value="input")
        compass_username = user_inputs[0]
        password = user_inputs[1]
        submit_button = self.driver.find_element(by=By.ID, value="btnLogin")

        compass_username.send_keys(username)
        password.send_keys(sk_password)
        submit_button.click()

    @log_decorator
    def login_sk(self) -> None:
        """
        Method that log in user to sk compass
        log in detail are passed automatically from .env file

        :return None
        """
        time.sleep(1)
        user_inputs = self.driver.find_elements(by=By.TAG_NAME, value="input")
        compass_username = user_inputs[0]
        password = user_inputs[1]
        submit_button = self.driver.find_element(by=By.ID, value="btnLogin")

        compass_username.send_keys(username)
        password.send_keys(sk_password)
        submit_button.click()

    @log_decorator
    def open_tabs(self, tab_count: int) -> None:
        """
        Method that opens new tabs in Chrome

        :param int tab_count: number of tabs to be opened
        :return None
        """
        for i in range(tab_count):
            self.driver.execute_script("window.open()")
            self.driver.switch_to.window(self.driver.window_handles[i + 1])

    @log_decorator
    def get_tab_objects(self) -> list:
        """
        Method that populates self.tabs list with Chrome tab objects

        :return: list self.tabs: list of opened Chrome tabs
        """
        tabs_list = [window for window in self.driver.window_handles[1::]]
        self.tabs = tabs_list

    @log_decorator
    def load_report_urls(self, data: dict) -> None:
        """
        Method that loads compass report urls in respective Chrome tabs

        :param dict data: metadata dictionary, from where urls are fetched
        :return: None
        """
        for i in range(len(data)):
            self.driver.switch_to.window(data[i]["tab"])
            self.driver.get(data[i]["path"])
            time.sleep(1)
