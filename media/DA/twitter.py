from setting.function import *
from setting.directory import *
from setting.report_date import *
from media.DA.DA_rule import *

import pandas as pd

def twitter_load():
    data = pd.read_csv(da_raw_dir + f'/twitter/raw_data/twitter_report_{day_1_yearmonth}.csv')
    data['매체'] = 'Twitter'

    twitter_data = data.copy()
    twitter_data['광고'] = twitter_data['광고 ID']
    twitter_data['OS'] = twitter_data['캠페인'].apply(lambda x : 'AOS' if 'AOS_' in x.upper() else 'iOS' if 'IOS_' in x.upper() else '-')
    twitter_data['조회'] = 0
    twitter_data['플랫폼'] = '-'
    twitter_data = twitter_data[DA_report_columns]
    twitter_data.to_csv(da_raw_dir + f'/twitter/twitter_{day_1_yearmonth}.csv', index=False, encoding = 'utf-8-sig')

def twitter_id_table():
    data = pd.read_csv(da_raw_dir + f'/twitter/raw_data/twitter_report_{day_1_yearmonth}.csv')
    columns = ['캠페인 ID', '캠페인', '광고그룹 ID', '광고그룹', '광고 ID']
    id_data = data[columns]
    id_data = data.drop_duplicates(subset = ['캠페인 ID', '광고그룹 ID', '광고 ID'], keep='first')
    return id_data

def twitter_preprocess():
    data = monthly_data_read('DA', 'twitter')
    return data
