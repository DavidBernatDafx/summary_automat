import time
from pprint import pprint
from data_manager import CompassMetaData, VccCdrData, VccUserStateData
from time_manager import Dates
from browser_manager import Browser
from reports import De01, De02, S26, Cm08
from file_manager import FileManager
from vcc import VccCdr, VccUserState
import os

# instantiate data objects - for now compass URLs
cz_data = CompassMetaData("cz")
print("cz_data object created")
sk_data = CompassMetaData("sk")
print("sk_data object created")

# instantiate dates to fill compass forms
dates = Dates()
print("dates object created")

# # open Chrome browser
# cz_compass = Browser()
# # load cz compass main page
# cz_compass.load_cz_compass(cz_data.location)
# # login into cz compass
# cz_compass.login_cz()
# # open blank tabs for reports
# cz_compass.open_tabs(len(cz_data.report_paths))
# # get list of blank tabs objects
# cz_compass.get_tab_objects()
# print(cz_compass.tabs)
# # pass tabs list from browser to data
# cz_data.tabs = cz_compass.tabs
# print(cz_data.tabs)
# # generates data structure to further work with Chrome driver
# cz_data.generate_full_data()
# # loads cz reports urls in blank tabs
# cz_compass.load_report_urls(cz_data.data_dict)
#
#
# # creates report objects, calling all needed methods, pass in current driver
#
# de_01_cz = De01(driver=cz_compass.driver, data=cz_data.data_dict[0], start_date=dates.dates_str["month_start"],
#                 end_date=dates.dates_str["yesterday"], location=cz_data.location, division="4LifeDirectCzechRepublic")
# de01_file_cz = FileManager(src_file="DE01_Policies.xlsx", dest_file="DE01_Policies.xlsx")
#
# de_02_cz = De02(driver=cz_compass.driver, data=cz_data.data_dict[1], start_date=dates.dates_str["month_start"],
#                 end_date=dates.dates_str["yesterday"], location=cz_data.location)
# de02_file_cz = FileManager(src_file="DE02_Leads_Full.xlsx", dest_file="DE02_Leads.xlsx")
#
# s_26_cz = S26(driver=cz_compass.driver, data=cz_data.data_dict[2], start_date=dates.dates_str["year_start"],
#               location=cz_data.location)
# s26_file_cz = FileManager(src_file="S26_TimeToCall.xlsx", dest_file="S26_TimeToCall_CZ.xlsx")
#
# de_01_all_cz = De01(driver=cz_compass.driver, data=cz_data.data_dict[3], start_date=dates.dates_str["year_start"],
#                     end_date=dates.dates_str["yesterday"], location=cz_data.location,
#                     division="4LifeDirectCzechRepublic")
# de01_all_file_cz = FileManager(src_file="DE01_Policies.xlsx", dest_file="DE01_Policies_all.xlsx")
#
# cm_08_cz = Cm08(driver=cz_compass.driver, data=cz_data.data_dict[4], start_date=dates.dates_str["year_rider"],
#                 end_date=dates.dates_str["yesterday_rider"], location=cz_data.location)
# cm08_file_cz = FileManager(src_file="CM08_Rider_Upgrade.xlsx", dest_file="CM08_Rider_Upgrade_CZ.xlsx")
#
# cz_compass.driver.quit()
#
# # open Chrome browser
# sk_compass = Browser()
# # load cz compass main page
# sk_compass.load_sk_compass(sk_data.location)
# # login into cz compass
# sk_compass.login_sk()
# # open blank tabs for reports
# sk_compass.open_tabs(len(sk_data.report_paths))
# # get list of blank tabs objects
# sk_compass.get_tab_objects()
# print(sk_compass.tabs)
# # pass tabs list from browser to data
# sk_data.tabs = sk_compass.tabs
# print(sk_data.tabs)
# # generates data structure to further work with Chrome driver
# sk_data.generate_full_data()
# # loads cz reports urls in blank tabs
# sk_compass.load_report_urls(sk_data.data_dict)
#
# de_01_sk = De01(driver=sk_compass.driver, data=sk_data.data_dict[0], start_date=dates.dates_str["month_start"],
#                 end_date=dates.dates_str["yesterday"], location=sk_data.location, division="4LifeDirectSlovakia")
# de01_file_sk = FileManager(src_file="DE01_Policies.xlsx", dest_file="DE01_Policies_SK.xlsx")
#
# de_02_sk = De02(driver=sk_compass.driver, data=sk_data.data_dict[1], start_date=dates.dates_str["month_start"],
#                 end_date=dates.dates_str["yesterday"], location=sk_data.location)
# de02_file_sk = FileManager(src_file="DE02_Leads_Full.xlsx", dest_file="DE02_Leads_SK.xlsx")
#
# s_26_sk = S26(driver=sk_compass.driver, data=sk_data.data_dict[2], start_date=dates.dates_str["year_start"],
#               location=sk_data.location)
# s26_file_sk = FileManager(src_file="S26_TimeToCall.xlsx", dest_file="S26_TimeToCall_SK.xlsx")
#
# de_01_all_sk = De01(driver=sk_compass.driver, data=sk_data.data_dict[3], start_date=dates.dates_str["year_start"],
#                     end_date=dates.dates_str["yesterday"], location=sk_data.location, division="4LifeDirectSlovakia")
# de01_all_file_sk = FileManager(src_file="DE01_Policies.xlsx", dest_file="DE01_Policies_all_SK.xlsx")
#
# cm_08_sk = Cm08(driver=sk_compass.driver, data=sk_data.data_dict[4], start_date=dates.dates_str["year_rider"],
#                 end_date=dates.dates_str["yesterday_rider"], location=sk_data.location)
# cm08_file_sk = FileManager(src_file="CM08_Rider_Upgrade.xlsx", dest_file="CM08_Rider_Upgrade_SK.xlsx")
#
# sk_compass.driver.quit()


"""SECTION VCC"""

# cdr_41 = VccCdr(project_id=41, year=dates.dates_vcc_str["year"], month=dates.dates_vcc_str["month"])
# cdr_15 = VccCdr(project_id=15, year=dates.dates_vcc_str["year"], month=dates.dates_vcc_str["month"])
# cdr_32 = VccCdr(project_id=32, year=dates.dates_vcc_str["year"], month=dates.dates_vcc_str["month"])
# cdr_39 = VccCdr(project_id=39, year=dates.dates_vcc_str["year"], month=dates.dates_vcc_str["month"])
#
# data_41 = VccCdrData(cdr_41.cdr_data, xlsx_filename="cdr-41.xlsx")
# data_15 = VccCdrData(cdr_15.cdr_data, xlsx_filename="cdr-15.xlsx")
# data_32 = VccCdrData(cdr_32.cdr_data, xlsx_filename="cdr-32.xlsx")
# data_39 = VccCdrData(cdr_39.cdr_data, xlsx_filename="cdr-39.xlsx")

vcc_user_state = VccUserState(from_date=dates.dates_vcc_str["start"], to_date=dates.dates_vcc_str["end"])
data_user_state = VccUserStateData(data=vcc_user_state.log_data, xlsx_filename="user-state.xlsx")



