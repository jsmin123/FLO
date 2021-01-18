from setting.function import *
from setting.directory import *
from setting.report_date import *
from media.DA.DA_rule import *

import pandas as pd

def facebook_load():
    data = pd.read_csv(da_raw_dir + f'/facebook/raw_data/facebook_report_{day_1_yearmonth}.csv')
    data['매체'] = 'Facebook'

    facebook_raw = data.rename(columns = {'광고세트' : '광고그룹',
                                          '게재지면' : '플랫폼',
                                          '링크 클릭' : '클릭',
                                          '동영상 3초 이상 재생' : '조회'})
    facebook_raw['OS'] = facebook_raw['광고그룹'].apply(lambda x : 'AOS' if 'AOS' in str(x).upper() else 'iOS' if 'IOS' in str(x).upper() else '알수없음')
    facebook_raw = facebook_raw[DA_report_columns]
    facebook_raw.to_csv(da_raw_dir + f'/facebook/facebook_{day_1_yearmonth}.csv', index=False, encoding = 'utf-8-sig')

def facebook_preprocess():
    data = monthly_data_read('DA', 'facebook')
    return data
