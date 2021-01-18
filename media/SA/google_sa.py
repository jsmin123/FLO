from setting.function import *
from setting.directory import *
from setting.report_date import *
from media.SA.SA_rule import *

import pandas as pd

def google_sa_load():
    data = pd.read_csv(sa_raw_dir + f'/google_sa/raw_data/google_ads_sa_report_{day_1_yearmonth}.csv')
    data['매체'] = 'Google_SA'
    data['플랫폼'] = 'M'
    data['광고'] = data['광고 ID']

    google_raw = data.copy()
    google_raw = google_raw[SA_report_columns + ['광고']]
    google_raw.to_csv(sa_raw_dir + f'/google_sa/google_sa_{day_1_yearmonth}.csv', index=False, encoding = 'utf-8-sig')

    # 그냥 다 합쳐서 보기