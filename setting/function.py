import pandas as pd
from setting.directory import *
from setting.report_date import *

def media_raw_read(media):
    file_name = media_raw_dir + f'/{media}/{media}_{day_1_yearmonth}.csv'
    raw_data = pd.read_csv(file_name)
    return raw_data

