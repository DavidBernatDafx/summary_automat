import os
import time

import xlwings as xl
from openpyxl import load_workbook, Workbook, worksheet
import datetime as dt
import os
from dotenv import load_dotenv
from decorators import log_decorator

load_dotenv("_env/.env")
summary_path = os.getenv("SUMMARY_PATH")
program_path = os.getenv("PROGRAM_PATH")

cdr_39_path = f"{program_path}/data/cdr-39.xlsx"
user_state_path = f"{program_path}/data/user-state.xlsx"
vcc_path = f"{summary_path}/VCC.xlsx"


@log_decorator
def create_worksheets(path: str, sheets_names: list):
    wb = load_workbook(filename=path)
    ws_list = [{"sheet": wb[sheet], "num_rows": wb[sheet].max_row} for sheet in sheets_names]
    return ws_list, wb


@log_decorator
def delete_content(workbook: tuple):
    sheets = workbook[0]
    for sheet in sheets:
        for row in sheet["sheet"]:
            for cell in row:
                cell.value = None


@log_decorator
def copy_content(cdr_data: tuple, user_log_data: tuple, vcc_data: tuple, export_file: str):
    cdr_source = cdr_data[0][0]["sheet"]
    user_log_source = user_log_data[0][0]["sheet"]
    cdr_dest = vcc_data[0][0]["sheet"]
    user_log_dest = vcc_data[0][1]["sheet"]

    for row in cdr_source["A:AK"]:
        for cell in row:
            cdr_dest[cell.coordinate].value = cell.value

    for row in user_log_source["A:I"]:
        for cell in row:
            user_log_dest[cell.coordinate].value = cell.value

    vcc_data[1].save(export_file)
    vcc_data[1].close()


def excel_manipulation():
    cdr_39 = create_worksheets(path=cdr_39_path, sheets_names=["Sheet1"])
    cdr_39[1].close()
    print(cdr_39)

    user_log = create_worksheets(path=user_state_path, sheets_names=["Sheet1"])
    user_log[1].close()
    print(user_log)

    vcc = create_worksheets(path=vcc_path, sheets_names=["infoline_zdroj", "List2"])
    print(vcc)

    delete_content(vcc)

    copy_content(cdr_data=cdr_39, user_log_data=user_log, vcc_data=vcc, export_file=vcc_path)

    os.remove(cdr_39_path)
    os.remove(user_state_path)


def run_excel_macros():
    yesterday = dt.datetime.now() - dt.timedelta(days=1)
    summary = xl.Book(f"{summary_path}/SummaryReport.xlsm")
    sheet = summary.sheets[1]
    date_cell = sheet.range("D2")
    date_cell.value = yesterday

    macro_1 = summary.macro("Module35.Makro1_data_den")
    macro_2 = summary.macro("Module16.Makro4_efficiency")

    print("Running Makro1_data_den")
    macro_1()
    print("Finished: OK")

    print("Running Makro4_efficiency")
    macro_2()
    print("Finished: OK")

    summary.save()
    summary.close()
    time.sleep(5)
    summary.app.kill()
