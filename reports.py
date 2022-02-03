from decorators import log_decorator
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


class De01:

    def __init__(self, driver, data: dict, start_date: str, end_date: str, location: str):
        self.start_date = start_date
        self.end_date = end_date
        self.filter_by = "CreateDt"
        self.division = "4LifeDirectCzechRepublic"
        self.premium_no = "1"
        self.location = location
        self.driver = driver
        self.driver.switch_to.window(data["tab"])
        self.elements = {}
        self.find_form_elements()
        self.fill_form()
        self.save_report()

    @log_decorator
    def find_form_elements(self):
        self.elements = {
            "start_date_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl03_txtValue"),
            "end_date_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl05_txtValue"),
            "filter_by_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl07_ddValue"),
            "division_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl11_ddValue"),
            "premium_no_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl09_txtValue"),
            "free_policies_box": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl13_rbTrue"),
            "submit_button": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl00"),
        }

    @log_decorator
    def fill_form(self):
        self.elements["start_date_field"].send_keys(self.start_date)
        self.elements["end_date_field"].send_keys(self.end_date)
        self.elements["filter_by_field"].send_keys(self.filter_by)
        self.elements["division_field"].send_keys(self.division)
        self.elements["premium_no_field"].send_keys(self.premium_no)
        self.elements["free_policies_box"].click()
        time.sleep(1)
        self.elements["submit_button"].click()
        time.sleep(1)

    @log_decorator
    def save_report(self):
        save_button = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl04_ctl00_ButtonImgDown")
        # trigger = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl00_TotalPages").text.strip(" ?")
        save_button.click()
        while True:
            trigger = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl00_TotalPages").text.strip(" ?")
            print(trigger)
            if trigger != "0":
                print("Report is generated.")
                save_button.click()
                ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
                print("Saving report.")
                break
            else:
                time.sleep(5)


class De02:

    def __init__(self, driver, data: dict, start_date: str, end_date: str, location: str):
        self.start_date = start_date
        self.end_date = end_date
        self.lead_types = "SMS Lead,Web Lead,Info Line Lead,CRO Lead,Enquirer Lead,Referral Lead,Online Lead," \
                          "Imported Lead,Duplicate Lead,Bulk Mailer Lead,Referral Plus Lead,First Year Lead," \
                          "Paid Only Lead,Free Only Lead,Point Of Sale,CS Lead,Affiliate Lead,Web External Lead"
        self.include_duplicates = "Yes"
        self.location = location
        self.driver = driver
        self.driver.switch_to.window(data["tab"])
        self.elements = {}
        self.find_form_elements()
        self.fill_form()
        self.save_report()

    @log_decorator
    def find_form_elements(self):
        self.elements = {
            "start_date_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl03_txtValue"),
            "end_date_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl05_txtValue"),
            "lead_types_dropdown": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl07_ctl01"),
            "leads_checkbox": None,
            "include_duplicates_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl09_ddValue"),
            "submit_button": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl00")
        }

    @log_decorator
    def fill_form(self):
        self.elements["start_date_field"].send_keys(self.start_date)
        self.elements["end_date_field"].send_keys(self.end_date)
        self.elements["lead_types_dropdown"].click()
        time.sleep(1)
        self.elements["leads_checkbox"] = self.driver.find_element(by=By.ID,
                                                                   value="ReportViewer1_ctl08_ctl07_divDropDown_ctl00")
        time.sleep(1)
        self.elements["leads_checkbox"].click()
        self.elements["include_duplicates_field"].send_keys(self.include_duplicates)
        time.sleep(1)
        self.elements["submit_button"].click()
        time.sleep(1)

    @log_decorator
    def save_report(self):
        save_button = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl04_ctl00_ButtonImgDown")
        # trigger = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl00_TotalPages").text.strip(" ?")
        save_button.click()
        while True:
            trigger = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl00_TotalPages").text.strip(" ?")
            print(trigger)
            if trigger != "0":
                print("Report is generated.")
                save_button.click()
                ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
                print("Saving report.")
                break
            else:
                time.sleep(5)


class S26:

    def __init__(self, driver, data: dict, start_date: str, location: str):
        self.driver = driver
        self.start_date = start_date
        self.location = location
        self.driver.switch_to.window(data["tab"])
        self.elements = {}
        self.find_form_elements()
        self.fill_form()
        self.save_report()

    @log_decorator
    def find_form_elements(self):
        self.elements = {
            "current_time_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl03_ddValue")}

    @log_decorator
    def fill_form(self):
        self.elements["current_time_field"].click()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
        time.sleep(5)
        self.elements["start_date_field"] = self.driver.find_element(by=By.ID,
                                                                     value="ReportViewer1_ctl08_ctl05_txtValue")
        ActionChains(self.driver).double_click(self.elements["start_date_field"]).send_keys(Keys.DELETE).perform()
        self.elements["start_date_field"].send_keys(self.start_date)
        time.sleep(3)
        self.elements["submit_button"] = self.driver.find_element(by=By.ID,
                                                                  value="ReportViewer1_ctl08_ctl00")
        self.elements["submit_button"].click()
        time.sleep(3)
        self.elements["submit_button"] = self.driver.find_element(by=By.ID,
                                                                  value="ReportViewer1_ctl08_ctl00")
        time.sleep(3)
        self.elements["submit_button"].click()
        time.sleep(10)

    @log_decorator
    def save_report(self):
        save_button = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl04_ctl00_ButtonImgDown")
        # trigger = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl00_TotalPages").text.strip(" ?")
        save_button.click()
        while True:
            trigger = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl00_TotalPages").text.strip(" ?")
            print(trigger)
            if trigger != "0":
                print("Report is generated.")
                save_button.click()
                ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
                print("Saving report.")
                break
            else:
                time.sleep(5)


class Cm08:

    def __init__(self, driver, data: dict, start_date: str, end_date: str, location: str):
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.driver = driver
        self.driver.switch_to.window(data["tab"])
        self.elements = {}
        self.find_form_elements()
        self.fill_form()
        self.save_report()

    @log_decorator
    def find_form_elements(self):
        self.elements = {
            "start_date_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl03_txtValue"),
            "end_date_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl05_txtValue"),
            "submit_button": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl00")
        }

    @log_decorator
    def fill_form(self):
        ActionChains(self.driver).double_click(self.elements["start_date_field"]).send_keys(Keys.DELETE).perform()
        self.elements["start_date_field"].send_keys(self.start_date)
        self.elements["end_date_field"].send_keys(self.end_date)
        self.elements["submit_button"].click()
        time.sleep(1)

    @log_decorator
    def save_report(self):
        save_button = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl04_ctl00_ButtonImgDown")
        # trigger = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl00_TotalPages").text.strip(" ?")
        save_button.click()
        while True:
            trigger = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl00_TotalPages").text.strip(" ?")
            print(trigger)
            if trigger != "0":
                print("Report is generated.")
                save_button.click()
                ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
                print("Saving report.")
                break
            else:
                time.sleep(5)
