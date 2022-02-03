import time
from pprint import pprint
from data_manager import Data
from time_manager import Dates
from browser_manager import Browser
from reports import De01, De02, S26, Cm08
from file_manager import FileManager
import os

# instantiate data objects - for now compass URLs
cz_data = Data("cz")
print("cz_data object created")
sk_data = Data("sk")
print("sk_data object created")

# instantiate dates to fill compass forms
dates = Dates()
print("dates object created")

# open Chrome browser
cz_compass = Browser()
# load cz compass main page
cz_compass.load_cz_compass(cz_data.location)
# login into cz compass
cz_compass.login_cz()
# open blank tabs for reports
cz_compass.open_tabs(len(cz_data.report_paths))
# get list of blank tabs objects
cz_compass.get_tab_objects()
print(cz_compass.tabs)
# pass tabs list from browser to data
cz_data.tabs = cz_compass.tabs
print(cz_data.tabs)
# generates data structure to further work with Chrome driver
cz_data.generate_full_data()
# loads cz reports urls in blank tabs
cz_compass.load_report_urls(cz_data.data_dict)


# creates report objects, calling all needed methods, pass in current driver

de_01 = De01(driver=cz_compass.driver, data=cz_data.data_dict[0], start_date=dates.dates_str["month_start"],
             end_date=dates.dates_str["yesterday"], location=cz_data.location)
de01_file = FileManager(src_file="DE01_Policies.xlsx", dest_file="DE01_Policies.xlsx")

de_02 = De02(driver=cz_compass.driver, data=cz_data.data_dict[1], start_date=dates.dates_str["month_start"],
             end_date=dates.dates_str["yesterday"], location=cz_data.location)
de02_file = FileManager(src_file="DE02_Leads_Full.xlsx", dest_file="DE02_Leads.xlsx")

s_26 = S26(driver=cz_compass.driver, data=cz_data.data_dict[2], start_date=dates.dates_str["month_start"],
           location=cz_data.location)
s26_file = FileManager(src_file="S26_TimeToCall.xlsx", dest_file="S26_TimeToCall_CZ.xlsx")

de_01_all = De01(driver=cz_compass.driver, data=cz_data.data_dict[3], start_date=dates.dates_str["year_start"],
                 end_date=dates.dates_str["yesterday"], location=cz_data.location)
de01_all_file = FileManager(src_file="DE01_Policies.xlsx", dest_file="DE01_Policies_all.xlsx")

cm_08 = Cm08(driver=cz_compass.driver, data=cz_data.data_dict[4], start_date=dates.dates_str["year_rider"],
             end_date=dates.dates_str["yesterday_rider"], location=cz_data.location)
cm08_file = FileManager(src_file="CM08_Rider_Upgrade.xlsx", dest_file="CM08_Rider_Upgrade_CZ.xlsx")

cz_compass.driver.quit()
