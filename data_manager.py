import os
from dotenv import load_dotenv
from decorators import log_decorator
from pprint import pprint

load_dotenv("_env/.env")
URL_BASE = os.getenv("url")

report_url_appendices = ["ReportViewer.aspx?reportId=67&report=DE01_Policies",
                         "ReportViewer.aspx?reportId=169&report=DE02_Leads_Full",
                         "ReportViewer.aspx?reportId=161&report=S26_TimeToCall",
                         "ReportViewer.aspx?reportId=69&report=DE03_DiaryItems",
                         "ReportViewer.aspx?reportId=67&report=DE01_Policies",
                         "ReportViewer.aspx?reportId=172&report=CM08_Rider_Upgrade"
                         ]


class Data:

    def __init__(self, location: str):
        self.location = location
        self.report_paths = []
        self.generate_report_paths()
        self.tabs = []
        self.data_dict = {}

    @log_decorator
    def generate_report_paths(self):
        self.report_paths = [f"{URL_BASE}{self.location}/{rep}" for rep in report_url_appendices]
        pprint(self.report_paths)

    @log_decorator
    def generate_full_data(self):
        if len(self.report_paths) == len(self.tabs):
            self.data_dict = {i:{"path": self.report_paths[i], "tab": self.tabs[i]}
                              for i in range(len(self.report_paths))
                              }
        print(self.data_dict)



