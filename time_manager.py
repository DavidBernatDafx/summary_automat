from datetime import datetime, timedelta
from decorators import log_decorator


now = datetime.now()
yesterday = now - timedelta(days=1)
yesterday_rider = yesterday + timedelta(days=1)
month_start = yesterday.replace(day=1)
year_start = yesterday.replace(day=1, month=1)
year_rider = year_start.replace(month=7)


class Dates:

    def __init__(self):
        self.dates = {
            "yesterday": yesterday,
            "yesterday_rider": yesterday_rider,
            "month_start": month_start,
            "year_start": year_start,
            "year_rider": year_rider,
        }
        self.dates_str = {}
        self.convert()

    @log_decorator
    def convert(self,):
        self.dates_str = {k: v.strftime("%d.%m.%Y") for k, v in self.dates.items()}
