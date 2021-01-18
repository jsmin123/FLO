import pandas as pd
from setting.function import *
from setting.directory import *
from setting.report_date import *

def tracker_data_load():
    result = pd.DataFrame()
    day = start_day
    while day < today :
        date = day.strftime('%Y-%m-%d')
        ua_data = pd.read_csv(tracker_raw_dir + f'/UA/{date}.csv', low_memory=False)
        re_data = pd.read_csv(tracker_raw_dir + f'/RE/{date}.csv', low_memory=False)

        ua_data['구분'] = 'UA'
        re_data['구분'] = 'RE'

        result = pd.concat([result, ua_data, re_data], sort = False)

        day = day + datetime.timedelta(1)

    result.to_csv(tracker_raw_dir + f'/apps_{day_1_yearmonth}.csv', index=False, encoding='utf-8-sig')
    print(f'AppsFlyer {day_1.month}월 Raw Data 적재 완료')
