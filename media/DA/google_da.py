from setting.function import *
from setting.directory import *
from setting.report_date import *
from media.DA.DA_rule import *

import pandas as pd

def google_da_load():
    data = pd.read_csv(da_raw_dir + f'/google_da/raw_data/google_ads_da_report_{day_1_yearmonth}.csv')
    data['매체'] = data['캠페인 유형'].apply(lambda x : 'Google_AC' if x=='MULTI_CHANNEL' else 'GDN' if x in ['DISPLAY', 'UNKNOWN'] else '알수없음')

    google_raw = data.rename(columns = {'네트워크(검색 파트너 포함)' : '플랫폼'})
    google_raw['조회'] = 0
    google_raw['광고'] = google_raw['광고그룹']
    google_raw['OS'] ='-'

    google_raw = google_raw[DA_report_columns]
    google_raw.to_csv(da_raw_dir + f'/google_da/google_da_{day_1_yearmonth}.csv', index=False, encoding = 'utf-8-sig')

    google_raw['플랫폼'].value_counts()

def google_ac_preprocess():
    da_data = monthly_data_read('DA','google_da')
    da_data_ac = da_data.loc[da_data['매체']=='Google_AC']
    da_data_ac['플랫폼'] = da_data_ac['플랫폼'].apply(lambda x : 'UAC_Search' if 'SEARCH' in str(x) else x)
    da_data_ac['플랫폼'] = da_data_ac['플랫폼'].apply(lambda x : 'UAC_Display' if 'CONTENT' in str(x) else x)
    sa_data = monthly_data_read('SA', 'google_sa')
    sa_data['플랫폼'] = 'Search'
    ac_data = pd.concat([da_data_ac, sa_data], sort= False)
    ac_data['OS'] = 'AOS'
    ac_data['광고'] = ac_data['광고그룹']
    ac_data['매체'] = 'Google_AC'
    return ac_data

def gdn_preprocess():
    google_da_data = monthly_data_read('DA', 'google_da')
    gdn_data = google_da_data.loc[google_da_data['매체']=='GDN']
    gdn_data['OS'] = 'AOS'


def google_id_table():
    da_data = pd.read_csv(da_raw_dir + f'/google_da/raw_data/google_ads_da_report_{day_1_yearmonth}.csv')
    sa_data = pd.read_csv(sa_raw_dir + f'/google_sa/raw_data/google_ads_sa_report_{day_1_yearmonth}.csv')

    google_data = pd.concat([da_data, sa_data], sort= False)
    columns = ['캠페인 ID', '캠페인', '광고그룹 ID', '광고그룹', '광고 ID']
    google_data = google_data[columns]
    google_id_data = google_data.drop_duplicates(subset = ['캠페인 ID', '광고그룹 ID', '광고 ID'], keep='first')

    return google_id_data
