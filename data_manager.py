import os
from dotenv import load_dotenv
from decorators import log_decorator
import datetime as dt
from pprint import pprint
import pandas as pd
from time_manager import convert_duration, convert_time

load_dotenv("_env/.env")
url_base = os.getenv("URL")

report_url_appendices = ["ReportViewer.aspx?reportId=67&report=DE01_Policies",
                         "ReportViewer.aspx?reportId=169&report=DE02_Leads_Full",
                         "ReportViewer.aspx?reportId=161&report=S26_TimeToCall",
                         "ReportViewer.aspx?reportId=67&report=DE01_Policies",
                         "ReportViewer.aspx?reportId=172&report=CM08_Rider_Upgrade"
                         ]


class CompassMetaData:

    def __init__(self, location: str):
        self.location = location
        self.report_paths = []
        self.generate_report_paths()
        self.tabs = []
        self.data_dict = {}

    @log_decorator
    def generate_report_paths(self):
        self.report_paths = [f"{url_base}{self.location}/{rep}" for rep in report_url_appendices]
        pprint(self.report_paths)

    @log_decorator
    def generate_full_data(self):
        if len(self.report_paths) == len(self.tabs):
            self.data_dict = {i: {"path": self.report_paths[i], "tab": self.tabs[i]}
                              for i in range(len(self.report_paths))
                              }
        print(self.data_dict)


class VccCdrData:

    def __init__(self, vcc_data: list, xlsx_filename: str):

        src_col_names = ["uuid", "shortid", "projectid", "source", "destination", "direction", "userfullname",
                         "numberid", "queue_label", "start_ts", "billing_ts", "next_contact", "prework",
                         "ringtime", "billingtime", "talktime", "queuetime", "beforequeuetime",
                         "disposition_export_name", "dispositionreach_label", "dispositionstatus_label",
                         "disposition_comment", "dialermode_label", "dc", "vcc_score", "hangup_disposition",
                         "afterwork", "holdtime", "sum_work"]
        exp_col_names = ["UUID", "Short Call ID", "Project ID", "Source", "Destination", "Direction", "Agent",
                         "Record ID", "Queue", "Start/Answer Time", "Billing Start Time", "Callback Date",
                         "Prework Time", "Ring Time", "Billable Time", "Talk Time", "Queue Time",
                         "Time Before Queue", "Disposition", "Disposition Outcome", "Disposition Type",
                         "Disposition note", "Dialing Mode", "Disconnect Cause Code", "Scores", "Hung Up By",
                         "Afterwork Time", "Hold Status", "Handling Time"]
        convert_time_cols = ["Ring Time", "Billable Time", "Talk Time", "Queue Time", "Time Before Queue",
                             "Hold Status", "Afterwork Time", "Prework Time"]
        convert_str_cols = ["Hung Up By"]
        convert_phone_cols = ["Source", "Destination"]
        convert_disposition_cols = ["disposition_label", "Disposition"]

        self.vcc_data = vcc_data
        self.source_df = pd.DataFrame(self.vcc_data)
        print(self.source_df.shape)
        self.rename_columns(old=src_col_names, new=exp_col_names)
        self.converted_df = self.convert_data(time_cols=convert_time_cols,
                                              data_cols=convert_str_cols,
                                              phone_cols=convert_phone_cols,
                                              disp_cols=convert_disposition_cols)
        print(self.converted_df["Talk Time"])
        self.export_df = self.create_export_dataframe()
        self.create_excel(filename=xlsx_filename)

    @log_decorator
    def rename_columns(self, old: list, new: list):
        col_dict = {old[i]: new[i] for i in range(len(old)) if len(old) == len(new)}
        self.source_df.rename(columns=col_dict, inplace=True)

    @log_decorator
    def convert_data(self, time_cols: list, data_cols: list, phone_cols: list, disp_cols: list):
        df_dict = self.source_df.to_dict()

        for col in time_cols:
            for k, v in df_dict[col].items():
                df_dict[col][k] = convert_duration(v)

        for col in data_cols:
            for k, v in df_dict[col].items():
                if v == "operator":
                    df_dict[col][k] = "Agent"
                elif v == "customer":
                    df_dict[col][k] = "Customer"

        for col in phone_cols:
            for k, v in df_dict[col].items():
                if v == "0000000000":
                    df_dict[col][k] = "0"

        for k, v in df_dict[disp_cols[1]].items():
            if not v:
                df_dict[disp_cols[1]][k] = df_dict[disp_cols[0]][k]

        return pd.DataFrame.from_dict(df_dict)

    @log_decorator
    def create_export_dataframe(self):
        export_df = self.converted_df[["UUID", "Short Call ID", "Project ID", "Source", "Destination", "Direction",
                                       "Agent", "Record ID", "Queue", "Start/Answer Time", "Billing Start Time",
                                       "Callback Date", "Prework Time", "Ring Time", "Billable Time", "Talk Time",
                                       "Hold Status", "Afterwork Time", "Handling Time", "Queue Time",
                                       "Time Before Queue", "Disposition", "Disposition Outcome", "Disposition Type",
                                       "Disposition note", "Dialing Mode", "Disconnect Cause Code", "Scores",
                                       "Hung Up By"]]
        export_df.insert(loc=2, column="Routing ID", value="global_routing")
        export_df.insert(loc=6, column="Phone Number Label", value="-")
        export_df.insert(loc=9, column="Extension", value=None)
        export_df.insert(loc=30, column="Rating (%)", value=None)
        export_df.insert(loc=33, column="Call Recording Status", value=None)
        export_df.insert(loc=34, column="Trashed By", value=None)
        export_df.insert(loc=35, column="Deleted By", value=None)
        export_df.insert(loc=35, column="Date Archived", value=None)

        return export_df
    @log_decorator
    def create_excel(self, filename: str):
        path = f"data/{filename}"
        # self.export_df.to_excel("data/vcc_data.xlsx", sheet_name=sheet_name, index=False,)
        # with pd.ExcelWriter("data/vcc_data.xlsx", engine="openpyxl") as writer:
        self.export_df.to_excel(path, index=False)


class VccUserStateData:

    def __init__(self, data: list, xlsx_filename: str):

        src_col_names = ["name", "prevtime", "prevstate", "duration", "projectid", "secondary_projects", "numberid"]
        exp_col_names = ["Username", "Time", "Status", "Time Spent in State", "Project ID", "Secondary Project ID",
                         "Record ID"]
        projects_dict = {"15": "Client Services - Outbound - CZ", "32": "Client Services - Outbound-SK",
                         "41": "Client Services - CZ_SK", "39": "Infoline - Inbound - CZ_SK", "23": "Sales - CZ",
                         "29": "Sales - SK", "82": "BJM_Active - CZ", "83": "BJM_nonActive - CZ",
                         "85": "BJM_Active - SK", "86": "BJM_nonActive - SK", "84": "Pre_call_Databases - CZ",
                         "87": "Pre_Call_Databases - SK", "72": "Appointment - CZ", "73": "Appointment - SK",
                         "76": "Transferred Calls - CZ", "79": "Transferred calls – SK",
                         "38": "Inbound - Infoline - CZ", "37": "Inbound - Infoline - SK"}

        self.vcc_data = data
        self.source_df = pd.DataFrame(self.vcc_data)
        pprint(self.source_df.shape)
        self.rename_columns(old=src_col_names, new=exp_col_names)
        self.converted_df = self.convert_data(projects=projects_dict)
        self.export_df = self.create_export_dataframe()
        self.create_excel(filename=xlsx_filename)

    @log_decorator
    def rename_columns(self, old: list, new: list):
        col_dict = {old[i]: new[i] for i in range (len(old)) if len(old) == len(new)}
        self.source_df.rename(columns=col_dict, inplace=True)
        self.source_df["Project"] = None
        self.source_df["Secondary Project"] = None

    @log_decorator
    def convert_data(self, projects: dict):
        df_dict = self.source_df.to_dict()

        for k, v in df_dict["Time Spent in State"].items():
            df_dict["Time Spent in State"][k] = convert_duration(int(v))

        for k, v in df_dict["Time"].items():
            df_dict["Time"][k] = convert_time(v)

        for k, v in df_dict["Status"].items():
            if v == "AUX":
                df_dict["Status"][k] = df_dict["auxid"][k]

        for k, v in df_dict["Project ID"].items():
            for key in projects.keys():
                if key == str(v):
                    df_dict["Project"][k] = projects[str(v)]

        for k, v in df_dict["Secondary Project ID"].items():
            pr_id_list = v.split(",")
            pr_names_list = list()

            for pr_id in pr_id_list:
                if pr_id in projects.keys():
                    pr_names_list.append(projects[pr_id])
                    
            df_dict["Secondary Project"][k] = ",".join(pr_names_list)

        return pd.DataFrame.from_dict(df_dict)

    @log_decorator
    def create_export_dataframe(self):
        export_df = self.converted_df[["Username", "Time", "Status", "Time Spent in State", "Project", "Project ID",
                                       "Secondary Project", "Secondary Project ID", "Record ID"]]
        return export_df

    @log_decorator
    def create_excel(self, filename: str):
        path = f"data/{filename}"
        # self.export_df.to_excel("data/vcc_data.xlsx", sheet_name=sheet_name, index=False,)
        # with pd.ExcelWriter("data/vcc_data.xlsx", engine="openpyxl") as writer:
        self.export_df.to_excel(path, index=False)



