import pandas as pd
from media.DA.facebook import *
from media.DA.DA_rule import *
from setting.spread_sheet import *
from report.report_rule import *

def da_dataset():
    # 나머지 데이터 준비되면 concat으로 바꾸기
    DA_data = facebook_load()
    DA_data['Media Source'] = DA_data['매체'].apply(lambda x : media_source_dict.get(x))
    DA_data['Platform'] = DA_data['광고그룹'].apply(lambda x : 'AOS' if 'AOS' in str(x).upper() else 'iOS' if 'IOS' in str(x).upper() else '알수없음')

    index = index_sheet()
    category_index = index[['Media Source', '소재', '캠페인 구분']]

    DA_data_labeling = DA_data.merge(category_index, on = ['Media Source', '소재'], how = 'left')


    pivot_columns = ['캠페인 구분', '매체','Media Source', 'Platform', '날짜', '캠페인', '광고그룹', '소재']
    DA_data_pivot = DA_data_labeling.pivot_table(index = pivot_columns, values = DA_value_columns, aggfunc = 'sum')
    DA_data_pivot = DA_data_pivot.reset_index()



