from setting.function import *
from setting.directory import *
from setting.report_date import *
from media.SA.SA_rule import *

import pandas as pd


def naver_sa_load():
    data = pd.read_csv(sa_raw_dir + f'/naver_sa/raw_data/naver_report_{day_1_yearmonth}.csv')
    data['매체'] = 'Naver_SA'
    data['플랫폼'] = data['OS'].apply(lambda x: 'M' if x == 'M' else 'PC')

    naver_raw = data.rename(columns = {'비용(VAT 포함)' : '비용'})
    naver_raw = naver_raw[SA_report_columns]
    naver_raw.to_csv(sa_raw_dir + f'/naver_sa/naver_{day_1_yearmonth}.csv', index=False, encoding='utf-8-sig')
