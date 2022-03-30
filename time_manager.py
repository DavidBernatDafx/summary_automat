from datetime import datetime, timedelta
from decorators import log_decorator
from time import sleep


now = datetime.now()
yesterday = now - timedelta(days=1)
yesterday_rider = yesterday + timedelta(days=1)
month_start = yesterday.replace(day=1)
year_start = yesterday.replace(day=1, month=1)
year_rider = year_start.replace(month=1)


class Dates:
    """
    Class that represents all needed dates for compass report forms and VCC API requests

    Attributes
    ----------

    dates : dict
        dictionary of dates for compass forms in datetime format
    dates_vcc : dict
        dictionary of dates for VCC API in str format
    dates_str : dict
        dictionary of dates for compass forms in str format
    dates_vcc_str : dict
        dictionary of converted dates for VCC API in str format

    Methods
    -------

    get_last_bd()
        method appends last business day to dates dict in case of yesterday is not business day
    convert()
        converts dates dict items to str and populates dates_str dict
    convert_vcc()
        converts dates_vcc items and populates dates_vcc_str dict
    """

    def __init__(self):
        self.dates = {
            "yesterday": yesterday,
            "yesterday_rider": yesterday_rider,
            "month_start": month_start,
            "year_start": year_start,
            "year_rider": year_rider,
        }

        self.dates_vcc = {
            "year": str(yesterday.year),
            "month": str(yesterday.month),
            "day": str(month_start.day),
            "month_to": str(now.month),
            "day_to": str(now.day),
        }
        self.get_last_bd()
        self.check_time()
        self.dates_str = {}
        self.convert()
        self.dates_vcc_str = {}
        self.convert_vcc()

    def __repr__(self):
        return f"<Dates for {datetime.strftime(self.dates['yesterday'], '%d.%m.%Y')}>"

    @log_decorator
    def check_time(self):
        hour = now.hour
        if hour >= 20:
            self.dates["yesterday"] += timedelta(days=1)
            self.dates["yesterday_rider"] += timedelta(days=1)
            self.dates["last_business_day"] += timedelta(days=1)

    @log_decorator
    def get_last_bd(self) -> datetime:
        day_name = self.dates["yesterday"].strftime("%A")
        if day_name == "Sunday":
            self.dates["last_business_day"] = self.dates["yesterday"] - timedelta(days=2)
        elif day_name == "Saturday":
            self.dates["last_business_day"] = self.dates["yesterday"] - timedelta(days=1)
        else:
            self.dates["last_business_day"] = self.dates["yesterday"]

    @log_decorator
    def convert(self,):
        self.dates_str = {k: v.strftime("%d.%m.%Y") for k, v in self.dates.items()}

    @log_decorator
    def convert_vcc(self):
        for k, v in self.dates_vcc.items():
            if len(v) == 1:
                self.dates_vcc_str[k] = f"0{v}"
            else:
                self.dates_vcc_str[k] = f"{v}"

        self.dates_vcc_str["year"] = self.dates_vcc["year"]
        self.dates_vcc_str["start"] = (self.dates_vcc_str["year"] +
                                       self.dates_vcc_str["month"] +
                                       self.dates_vcc_str["day"])
        self.dates_vcc_str["end"] = (self.dates_vcc_str["year"] +
                                     self.dates_vcc_str["month_to"] +
                                     self.dates_vcc_str["day_to"])


# def convert_duration(duration: float):
#     td = timedelta(seconds=int(duration))
#     return td


def convert_time(time: str) -> datetime:
    """
    Function converts str datetime objects and returns datetime objects

    :param str time: datetime str
    :return datetime : datetime
    """
    dt_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    return dt_time
