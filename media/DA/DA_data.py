import pandas as pd
from media.DA import *
from media.DA.DA_rule import *
from setting.spread_sheet import *
from report.report_rule import *
from media.DA import *

def da_dataset():
    # 나머지 데이터 준비되면 concat으로 바꾸기
    facebook_data = facebook.facebook_preprocess()
    google_ac_data = google_da.google_ac_preprocess()
    gdn_data = google_da.gdn_preprocess()
    twitter_data = twitter.twitter_preprocess()
    criteo_data = criteo.criteo_preprocess()
    sub_media_data = sub_media.sub_media_preprocess()

    # criteo_data = criteo.criteo_preprocess()

    DA_data = pd.concat([facebook_data, google_ac_data, gdn_data, twitter_data, criteo_data, sub_media_data], sort =False)

    # index = index_sheet()
    # category_index = index[['Media Source', '소재', '캠페인 구분']]
    #
    # DA_data_labeling = DA_data.merge(category_index, on = ['Media Source', '소재'], how = 'left')
    #
    #
    DA_data_pivot = DA_data.pivot_table(index = DA_pivot_columns, values = DA_value_columns, aggfunc = 'sum')
    DA_data_pivot = DA_data_pivot.reset_index()
    DA_data_pivot['media_source'] = DA_data_pivot['매체'].apply(lambda x : media_source_dict.get(x))
    DA_data_pivot['날짜'] = pd.to_datetime(DA_data_pivot['날짜']).dt.date
    return DA_data_pivot



