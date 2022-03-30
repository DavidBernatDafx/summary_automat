import os
import time
import xlwings as xl
from openpyxl import load_workbook, Workbook, worksheet
import datetime as dt
import os
from dotenv import load_dotenv
from decorators import log_decorator

# loading environment variables
load_dotenv("_env/.env")
summary_path = os.getenv("SUMMARY_PATH")
# program_path = os.getenv("PROGRAM_PATH")

cwd = os.getcwd()
cdr_39_path = os.path.join(cwd, "data", "cdr-39.xlsx")
user_state_path = os.path.join(cwd, "data", "user-state.xlsx")
# cdr_39_path = f"{program_path}/data/cdr-39.xlsx"
# user_state_path = f"{program_path}/data/user-state.xlsx"
vcc_path = f"{summary_path}/VCC.xlsx"


@log_decorator
def create_worksheets(path: str, sheets_names: list) -> tuple:
    """
    Function opens Excel file and populates sheet_names list with required Excel sheet objects

    param str path: path to Excel file
    param list sheets_names: list of Excel sheet names that populates sheet_list
    return: tuple ([sheet_list], workbook)
    """

    wb = xl.Book(path)
    ws_list = [wb.sheets[sheet] for sheet in sheets_names]
    return ws_list, wb


@log_decorator
def delete_content(workbook: tuple) -> None:
    """
    Function that delete content of passed list objects

    param tuple workbook: tuple representing Excel file ([sheet_list], workbook)
    return: None
    """

    sheets = workbook[0]
    for sheet in sheets:
        sheet.range("A:AK").value = None
    workbook[1].save()


@log_decorator
def copy_content(cdr_data: tuple, user_log_data: tuple, vcc_data: tuple, export_file: str) -> None:
    """
    Function that copy content of temp Excel workbook/sheets to destination Excel workbook/sheets

    param tuple cdr_data: tuple representing Excel file ([sheet_list], workbook)
    param user_log_data: tuple representing Excel file ([sheet_list], workbook)
    param vcc_data: tuple representing Excel file ([sheet_list], workbook)
    param export_file: tuple representing Excel file ([sheet_list], workbook)
    return: None
    """
    cdr_source = cdr_data[0][0]
    user_log_source = user_log_data[0][0]
    cdr_dest = vcc_data[0][0]
    user_log_dest = vcc_data[0][1]
    # print(cdr_source, user_log_source, cdr_dest, user_log_dest)

    cdr_data = cdr_source.range("A:AK")
    user_log_data = user_log_source.range("A:I")

    cdr_data.copy(cdr_dest.range("A:AK"))
    user_log_data.copy(user_log_dest.range("A:I"))

    cdr_dest.range("A:AK").value = cdr_data
    user_log_dest.range("A:I").value = user_log_data


@log_decorator
def excel_manipulation() -> None:
    """
    Function that executes desired Excel operations
    Creates temp Excel file tuples, deletes content of destination sheets, copy content from temp-source to destination
    sheets, save destination Excel file, close all Excel windows, terminates Excel driver and deletes temp Excel files

    :return: None
    """
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


def run_excel_macros(date: str) -> None:
    """
    Function that executes VBA macros in summary.xlsm
    Creates summary.xlsm object and default sheet, fills date of report to cell, run all 3 macros, saves file,
    closes Excel file, and terminates Excel driver

    :param str date: string representation of last business day date
    :return: None
    """

    app = xl.App()
    summary = xl.Book(f"{summary_path}/SummaryReport.xlsm")

    sheet = summary.sheets["Zadani"]

    print(f"Excel macros day: {date}")
    date_cell = sheet.range("D2")
    date_cell.value = date

    @log_decorator
    def run_macro(module: "str"):
        macro = summary.macro(module)
        macro()

    run_macro("Module38.Convert_vcc")
    run_macro("Module35.Makro1_data_den")
    run_macro("Module16.Makro4_efficiency")

    summary.save()
    summary.close()
    time.sleep(5)
    app.kill()


run_excel_macros(date="test")