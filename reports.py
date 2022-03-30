from decorators import log_decorator
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


class Report:
    """
    Class that represents chromedriver tab compass report object

    Attributes
    ----------
    None

    Methods
    -------
    save_report()
        method that checks in time controlled loop if report table is generated.
        When true it click download as xls html element.
    """

    def __init__(self):
        # self.no_report = False
        pass

    @log_decorator
    def save_report(self) -> None:
        """
        Method that checks in time controlled loop if report table is generated.
        When true it click download as xls html element.

        return: None
        """
        time.sleep(1)
        save_button = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl04_ctl00_ButtonImgDown")
        save_button.click()

        while True:
            trigger = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl00_TotalPages").text.strip(" ?")

            if trigger != "0":
                save_button = self.driver.find_element(by=By.ID, value="ReportViewer1_ctl09_ctl04_ctl00_ButtonImgDown")
                save_button.click()
                ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
                break
            else:
                time.sleep(5)


class De01(Report):
    """
    Subclass of Report class, that represents DE01 compass report

    Attributes
    ----------
    driver : object
        chrome webdriver object
    data : dict
        metadata passed from CompassMetaData.data_dict, contains tab object and url details
    start_date : str
        start date string to fill report form
    end_date : str
        end date string to fill report form
    division : str
        national division to fill report form
    elements : dict
        dictionary containing all needed html elements to interact with compass report webpage

    Methods
    -------
    find_form_elements()
        Method that finds all needed html elements to interact with compass report webpage
    fill_form()
        Method that fills form elements with class attributes
    """

    def __init__(self, driver, data: dict, start_date: str, end_date: str, division: str, loc: str):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.filter_by = "CreateDt"
        self.division = division
        self.premium_no = "1"
        self.driver = driver
        self.loc = loc
        self.driver.switch_to.window(data["tab"])
        self.elements = {}
        self.find_form_elements()
        self.fill_form()
        self.save_report()

    def __repr__(self):
        return f"<DE01.{self.loc} Chrome tab>"

    @log_decorator
    def find_form_elements(self) -> None:
        """
        Method that finds all needed html elements to interact with compass report webpage

        return: None
        """
        time.sleep(2)
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
    def fill_form(self) -> None:
        """
        Method that fills form elements with class attributes

        return: None
        """
        self.elements["start_date_field"].send_keys(self.start_date)
        self.elements["end_date_field"].send_keys(self.end_date)
        self.elements["filter_by_field"].send_keys(self.filter_by)
        self.elements["division_field"].send_keys(self.division)
        self.elements["premium_no_field"].send_keys(self.premium_no)
        self.elements["free_policies_box"].click()
        time.sleep(1)
        self.elements["submit_button"].click()
        time.sleep(1)


class De02(Report):
    """
    Subclass of Report class, that represents DE02 compass report

    Attributes
    ----------
    driver : object
        chrome webdriver object
    data : dict
        metadata passed from CompassMetaData.data_dict, contains tab object and url details
    start_date : str
        start date string to fill report form
    end_date : str
        end date string to fill report form
    elements : dict
        dictionary containing all needed html elements to interact with compass report webpage

    Methods
    -------
    find_form_elements()
        Method that finds all needed html elements to interact with compass report webpage
    fill_form()
        Method that fills form elements with class attributes
    """

    def __init__(self, driver, data: dict, start_date: str, end_date: str, loc: str):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.lead_types = "SMS Lead,Web Lead,Info Line Lead,CRO Lead,Enquirer Lead,Referral Lead,Online Lead," \
                          "Imported Lead,Duplicate Lead,Bulk Mailer Lead,Referral Plus Lead,First Year Lead," \
                          "Paid Only Lead,Free Only Lead,Point Of Sale,CS Lead,Affiliate Lead,Web External Lead"
        self.include_duplicates = "Yes"
        self.driver = driver
        self.loc = loc
        self.driver.switch_to.window(data["tab"])
        self.elements = {}
        self.find_form_elements()
        self.fill_form()
        self.save_report()

    def __repr__(self):
        return f"<DE02.{self.loc} Chrome tab>"

    @log_decorator
    def find_form_elements(self) -> None:
        """
        Method that finds all needed html elements to interact with compass report webpage

        return: None
        """
        time.sleep(2)
        self.elements = {
            "start_date_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl03_txtValue"),
            "end_date_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl05_txtValue"),
            "lead_types_dropdown": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl07_ctl01"),
            "leads_checkbox": None,
            "include_duplicates_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl09_ddValue"),
            "submit_button": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl00")
        }

    @log_decorator
    def fill_form(self) -> None:
        """
        Method that fills form elements with class attributes

        return: None
        """
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


class S26(Report):
    """
    Subclass of Report class, that represents S26 compass report

    Attributes
    ----------
    driver : object
        chrome webdriver object
    data : dict
        metadata passed from CompassMetaData.data_dict, contains tab object and url details
    start_date : str
        start date string to fill report form
    elements : dict
        dictionary containing all needed html elements to interact with compass report webpage

    Methods
    -------
    find_form_elements()
        Method that finds all needed html elements to interact with compass report webpage
    fill_form()
        Method that fills form elements with class attributes
    """

    def __init__(self, driver, data: dict, start_date: str, loc: str):
        super().__init__()
        self.driver = driver
        self.loc = loc
        self.start_date = start_date
        self.driver.switch_to.window(data["tab"])
        self.elements = {}
        self.find_form_elements()
        self.fill_form()
        self.save_report()

    def __repr__(self):
        return f"<S26.{self.loc} Chrome tab>"

    @log_decorator
    def find_form_elements(self) -> None:
        """
        Method that finds all needed html elements to interact with compass report webpage

        return: None
        """
        time.sleep(2)
        self.elements = {
            "current_time_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl03_ddValue")}

    @log_decorator
    def fill_form(self) -> None:
        """
        Method that fills form elements with class attributes

        return: None
        """
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


class Cm08(Report):
    """
    Subclass of Report class, that represents CM08 compass report

    Attributes
    ----------
    driver : object
        chrome webdriver object
    data : dict
        metadata passed from CompassMetaData.data_dict, contains tab object and url details
    start_date : str
        start date string to fill report form
    end_date : str
        end date string to fill report form
    elements : dict
        dictionary containing all needed html elements to interact with compass report webpage

    Methods
    -------
    find_form_elements()
        Method that finds all needed html elements to interact with compass report webpage
    fill_form()
        Method that fills form elements with class attributes
    """

    def __init__(self, driver, data: dict, start_date: str, end_date: str, loc: str):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.driver = driver
        self.loc = loc
        self.driver.switch_to.window(data["tab"])
        self.elements = {}
        self.find_form_elements()
        self.fill_form()
        self.save_report()

    def __repr__(self):
        return f"<CM08.{self.loc} Chrome tab>"

    @log_decorator
    def find_form_elements(self) -> None:
        """
        Method that finds all needed html elements to interact with compass report webpage

        return: None
        """
        time.sleep(2)
        self.elements = {
            "start_date_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl03_txtValue"),
            "end_date_field": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl05_txtValue"),
            "submit_button": self.driver.find_element(by=By.ID, value="ReportViewer1_ctl08_ctl00")
        }

    @log_decorator
    def fill_form(self) -> None:
        """
        Method that fills form elements with class attributes

        return: None
        """
        ActionChains(self.driver).double_click(self.elements["start_date_field"]).send_keys(Keys.DELETE).perform()
        self.elements["start_date_field"].send_keys(self.start_date)
        self.elements["end_date_field"].send_keys(self.end_date)
        self.elements["submit_button"].click()
        time.sleep(1)
