from datetime import timedelta
from datetime import date

today = date.today()
day_1 = today - timedelta(1)
day_1_yearmonth = day_1.strftime('%Y%m')