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


def create_worksheets(path: str, sheets_names: list):

    wb = xl.Book(path)
    ws_list = [wb.sheets[sheet] for sheet in sheets_names]
    return ws_list, wb


@log_decorator
def delete_content(workbook: tuple):
    sheets = workbook[0]
    for sheet in sheets:
        sheet.range("A:AK").clear()
    workbook[1].save()


@log_decorator
def copy_content(cdr_data: tuple, user_log_data: tuple, vcc_data: tuple, export_file: str):
    cdr_source = cdr_data[0][0]
    user_log_source = user_log_data[0][0]
    cdr_dest = vcc_data[0][0]
    user_log_dest = vcc_data[0][1]
    print(cdr_source, user_log_source, cdr_dest, user_log_dest)

    cdr_data = cdr_source.range("A:AK").value
    user_log_data = user_log_source.range("A:I").value

    cdr_dest.range("A:AK").value = cdr_data
    user_log_dest.range("A:I").value = user_log_data


@log_decorator
def excel_manipulation():
    app = xl.App()
    cdr_39 = create_worksheets(path=cdr_39_path, sheets_names=["Sheet1"])
    print(cdr_39)

    user_log = create_worksheets(path=user_state_path, sheets_names=["Sheet1"])
    print(user_log)

    vcc = create_worksheets(path=vcc_path, sheets_names=["List1", "List2"])
    print(vcc)

    delete_content(vcc)

    copy_content(cdr_data=cdr_39, user_log_data=user_log, vcc_data=vcc, export_file=vcc_path)

    vcc[1].save()
    vcc[1].close()
    cdr_39[1].close()
    user_log[1].close()
    app.kill()

    os.remove(cdr_39_path)
    os.remove(user_state_path)


def run_excel_macros(date: dt):
    app = xl.App()
    summary = xl.Book(f"{summary_path}/SummaryReport.xlsm")
    sheet = summary.sheets[1]
    date_cell = sheet.range("D2")
    date_cell.value = date

    macro_1 = summary.macro("Module35.Makro1_data_den")
    macro_2 = summary.macro("Module16.Makro4_efficiency")

    print("Running Makro1_data_den")
    macro_1()
    print("Finished: OK")
    time.sleep(10)
    print("Running Makro4_efficiency")
    macro_2()
    print("Finished: OK")

    summary.save()
    summary.close()
    time.sleep(5)
    app.kill()


