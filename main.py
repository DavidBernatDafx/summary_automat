from pprint import pprint
import datetime
import sys
import time
from data_manager import CompassMetaData, VccCdrData, VccUserStateData
from time_manager import Dates
from browser_manager import Browser
from reports import De01, De02, S26, Cm08
from file_manager import FileManager, check_files, cz_destination_files, sk_destination_files, copy_to_dropbox, \
    summary_path, dropbox_path
from vcc import VccCdr, VccUserState
from excel_manager import excel_manipulation, run_excel_macros
from comms_manager import send_notification
import os
import math
from logging_manager import Logger


script_start = datetime.datetime.now()

print(f"Starting summary automation script at: {script_start.strftime('%Y.%m.%d %H:%M')}")

# instantiate browser metadata objects - for now compass URLs
cz_data = CompassMetaData("cz")
sk_data = CompassMetaData("sk")

# instantiate dates to fill compass forms, vcc requests and excel interaction
dates = Dates()

"""CZ compass section"""
while not check_files(cz_destination_files):

    cz_compass = Browser()                              # open Chrome browser
    cz_compass.load_cz_compass(cz_data.location)        # load cz compass main page
    cz_compass.login_cz()                               # login into cz compass
    cz_compass.open_tabs(len(cz_data.report_paths))     # open blank tabs for reports
    cz_compass.get_tab_objects()                        # get list of blank tabs objects
    cz_data.tabs = cz_compass.tabs                      # pass tabs list from browser to data
    cz_data.generate_full_data()                        # generates data structure to further work with Chrome driver
    cz_compass.load_report_urls(cz_data.data_dict)      # loads cz reports urls in blank tabs

    # creates report objects, calling all needed methods, pass in current driver
    # ----------------------------------------------------------------------------------------------------------------
    de_01_cz = De01(driver=cz_compass.driver, data=cz_data.data_dict[0], start_date=dates.dates_str["month_start"],
                    end_date=dates.dates_str["yesterday"], division="4LifeDirectCzechRepublic", loc=cz_compass.loc)
    de01_file_cz = FileManager(src_file="DE01_Policies.xlsx", dest_file="DE01_Policies.xlsx")
    # ----------------------------------------------------------------------------------------------------------------
    de_02_cz = De02(driver=cz_compass.driver, data=cz_data.data_dict[1], start_date=dates.dates_str["month_start"],
                    end_date=dates.dates_str["yesterday"], loc=cz_compass.loc)
    de02_file_cz = FileManager(src_file="DE02_Leads_Full.xlsx", dest_file="DE02_Leads.xlsx")
    # ----------------------------------------------------------------------------------------------------------------
    s_26_cz = S26(driver=cz_compass.driver, data=cz_data.data_dict[2], start_date=dates.dates_str["year_start"],
                  loc=cz_compass.loc)
    s26_file_cz = FileManager(src_file="S26_TimeToCall.xlsx", dest_file="S26_TimeToCall_CZ.xlsx")
    # ----------------------------------------------------------------------------------------------------------------
    de_01_all_cz = De01(driver=cz_compass.driver, data=cz_data.data_dict[3], start_date=dates.dates_str["year_start"],
                        end_date=dates.dates_str["yesterday"], division="4LifeDirectCzechRepublic", loc=cz_compass.loc)
    de01_all_file_cz = FileManager(src_file="DE01_Policies.xlsx", dest_file="DE01_Policies_all.xlsx")
    # ----------------------------------------------------------------------------------------------------------------
    cm_08_cz = Cm08(driver=cz_compass.driver, data=cz_data.data_dict[4], start_date=dates.dates_str["year_rider"],
                    end_date=dates.dates_str["yesterday_rider"], loc=cz_compass.loc)
    cm08_file_cz = FileManager(src_file="CM08_Rider_Upgrade.xlsx", dest_file="CM08_Rider_Upgrade_CZ.xlsx")
    # ----------------------------------------------------------------------------------------------------------------
    cz_compass.driver.quit()


"""SK compass section"""
while not check_files(sk_destination_files):

    sk_compass = Browser()                              # open Chrome browser
    sk_compass.load_sk_compass(sk_data.location)        # load sk compass main page
    sk_compass.login_sk()                               # login into cz compass
    sk_compass.open_tabs(len(sk_data.report_paths))     # open blank tabs for reports
    sk_compass.get_tab_objects()                        # get list of blank tabs objects
    sk_data.tabs = sk_compass.tabs                      # pass tabs list from browser to data
    sk_data.generate_full_data()                        # generates data structure to further work with Chrome driver
    sk_compass.load_report_urls(sk_data.data_dict)      # loads cz reports urls in blank tabs

    # creates report objects, calling all needed methods, pass in current driver
    # ----------------------------------------------------------------------------------------------------------------
    de_01_sk = De01(driver=sk_compass.driver, data=sk_data.data_dict[0], start_date=dates.dates_str["month_start"],
                    end_date=dates.dates_str["yesterday"], division="4LifeDirectSlovakia", loc=sk_compass.loc)
    de01_file_sk = FileManager(src_file="DE01_Policies.xlsx", dest_file="DE01_Policies_SK.xlsx")
    # ----------------------------------------------------------------------------------------------------------------
    de_02_sk = De02(driver=sk_compass.driver, data=sk_data.data_dict[1], start_date=dates.dates_str["month_start"],
                    end_date=dates.dates_str["yesterday"], loc=sk_compass.loc)
    de02_file_sk = FileManager(src_file="DE02_Leads_Full.xlsx", dest_file="DE02_Leads_SK.xlsx")
    # ----------------------------------------------------------------------------------------------------------------
    s_26_sk = S26(driver=sk_compass.driver, data=sk_data.data_dict[2], start_date=dates.dates_str["year_start"],
                  loc=sk_compass.loc)
    s26_file_sk = FileManager(src_file="S26_TimeToCall.xlsx", dest_file="S26_TimeToCall_SK.xlsx")
    # ----------------------------------------------------------------------------------------------------------------
    de_01_all_sk = De01(driver=sk_compass.driver, data=sk_data.data_dict[3], start_date=dates.dates_str["year_start"],
                        end_date=dates.dates_str["yesterday"], division="4LifeDirectSlovakia", loc=sk_compass.loc)
    de01_all_file_sk = FileManager(src_file="DE01_Policies.xlsx", dest_file="DE01_Policies_all_SK.xlsx")
    # ----------------------------------------------------------------------------------------------------------------
    cm_08_sk = Cm08(driver=sk_compass.driver, data=sk_data.data_dict[4], start_date=dates.dates_str["year_rider"],
                    end_date=dates.dates_str["yesterday_rider"], loc=sk_compass.loc)
    cm08_file_sk = FileManager(src_file="CM08_Rider_Upgrade.xlsx", dest_file="CM08_Rider_Upgrade_SK.xlsx")
    # ----------------------------------------------------------------------------------------------------------------
    sk_compass.driver.quit()


"""VCC section"""
# get cdr log via VCC API request
cdr_39 = VccCdr(project_id=39, year=dates.dates_vcc_str["year"], month=dates.dates_vcc_str["month"])
# cdr_41 = VccCdr(project_id=41, year=dates.dates_vcc_str["year"], month=dates.dates_vcc_str["month"])
# cdr_15 = VccCdr(project_id=15, year=dates.dates_vcc_str["year"], month=dates.dates_vcc_str["month"])
# cdr_32 = VccCdr(project_id=32, year=dates.dates_vcc_str["year"], month=dates.dates_vcc_str["month"])

# process response data with pandas dataframe, then export to temporary .xls file
data_39 = VccCdrData(cdr_39.cdr_data, xlsx_filename="cdr-39.xlsx")
# data_41 = VccCdrData(cdr_41.cdr_data, xlsx_filename="cdr-41.xlsx")
# data_15 = VccCdrData(cdr_15.cdr_data, xlsx_filename="cdr-15.xlsx")
# data_32 = VccCdrData(cdr_32.cdr_data, xlsx_filename="cdr-32.xlsx")
# --------------------------------------------------------------------------------------------------------------------

# get user state log via VCC API request
vcc_user_state = VccUserState(from_date=dates.dates_vcc_str["start"], to_date=dates.dates_vcc_str["end"])
# process response data with pandas dataframe, then export to temporary .xls file
data_user_state = VccUserStateData(data=vcc_user_state.log_data, xlsx_filename="user-state.xlsx")

""" excel section"""
# clear vcc.xlsx old data, copy new data from temp .xlsx files, delete temp files
excel_manipulation()
time.sleep(5)
# fill yesterday date to summary.xlsm, then run 2 macros and save file
run_excel_macros(date=dates.dates_str["last_business_day"])

time.sleep(5)
copy_to_dropbox(src=summary_path, dest=dropbox_path)
time.sleep(5)
send_notification(date=dates.dates_str["last_business_day"])

scrip_end = datetime.datetime.now()
script_duration = scrip_end - script_start
minutes = math.floor(script_duration.total_seconds() / 60)
seconds = round(script_duration.total_seconds() % 60, 2)
print(f"Script finished in {minutes}:{seconds}")
