from datetime import datetime, timedelta
from decorators import log_decorator


now = datetime.now()
yesterday = now - timedelta(days=1)
yesterday_rider = yesterday + timedelta(days=1)
month_start = yesterday.replace(day=1)
year_start = yesterday.replace(day=1, month=1)
year_rider = year_start.replace(month=1)


class Dates:

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
        }

        self.dates_str = {}
        self.convert()
        self.dates_vcc_str = {}
        self.convert_vcc()
        print(self.dates_vcc_str)

    @log_decorator
    def convert(self,):
        self.dates_str = {k: v.strftime("%d.%m.%Y") for k, v in self.dates.items()}

    @log_decorator
    def convert_vcc(self):
        self.dates_vcc_str = {k: f"0{v}" for k, v in self.dates_vcc.items() if len(v) == 1}
        self.dates_vcc_str["year"] = self.dates_vcc["year"]


def convert_duration(duration: int):
    return str(timedelta(seconds=duration))

