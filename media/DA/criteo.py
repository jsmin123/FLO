from setting.function import *
from setting.directory import *
from setting.report_date import *
from media.DA.DA_rule import *

import pandas as pd

def criteo_load():
    data = pd.read_csv(da_raw_dir + f'/criteo/raw_data/criteo_report_{day_1_yearmonth}.csv')
    data['매체'] = 'Criteo'

    # 기준 바뀌면 말씀해주세요
    data['조회'] = 0
    data['광고그룹'] = ''
    data['광고'] = ''
    data['플랫폼'] = '-'
    criteo_raw = data[DA_report_columns]
    criteo_raw.to_csv(da_raw_dir + f'/criteo/criteo_{day_1_yearmonth}.csv', index=False, encoding = 'utf-8-sig')

def criteo_preprocess():
    data = monthly_data_read('DA', 'criteo')
    data.loc[data['캠페인'].str.count(pat = 'ADID') > 0, 'OS'] = \
        data['캠페인'].apply(lambda x : 'AOS' if 'AOS' in x.upper() else 'iOS' if 'IOS' in x.upper() else '-')
    data['캠페인'] = data['캠페인'].apply(
        lambda x: 'AOS' if 'Android' in x else 'iOS' if 'iOS' in x else 'ADID' if 'ADID' in x else x)
    data.loc[data['캠페인']!='ADID', 'OS'] = data['캠페인']
    return data