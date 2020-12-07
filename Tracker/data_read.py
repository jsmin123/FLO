import pandas as pd
from setting.function import *
from setting.directory import *
from setting.report_date import *

def install_raw_read():
    aos_file_name = tracker_raw_dir + f'/Install/AOS_{day_1_yearmonth}.csv'
    ios_file_name = tracker_raw_dir + f'/Install/iOS_{day_1_yearmonth}.csv'

    aos_raw = pd.read_csv(aos_file_name)
    ios_raw = pd.read_csv(ios_file_name)

    install_raw = pd.concat([aos_raw, ios_raw], sort = False)

    return install_raw
