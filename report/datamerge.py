from media.DA.DA_data import *
from Tracker.preprocess import *
from setting.directory import *

apps_da_raw = apps_da_rawdata()
da_data = da_dataset()

# 신규설치, 재설치, 재실행으로 나눠서 작업 필요 / 리인게이지먼트 = 재실행, 리어트리뷰션 = 재설치
install_table = event_table(apps_da_raw, event_name = 'install', column_name='신규설치')
re_install_table = event_table(apps_da_raw, event_name = 're-attribution', column_name='재설치')
re_exec_table = event_table(apps_da_raw, event_name='re-engagement', column_name='재실행')

temp = da_data.merge(install_table, on = ['media_source','날짜', 'OS','플랫폼', '캠페인', '광고그룹', '광고'], how = 'outer')
temp = temp.merge(re_install_table, on = ['media_source','날짜', 'OS','플랫폼', '캠페인', '광고그룹', '광고'], how = 'outer')
temp = temp.merge(re_exec_table, on = ['media_source','날짜', 'OS','플랫폼', '캠페인', '광고그룹', '광고'], how = 'outer')

temp.to_csv(download_dir + '/temp.csv', index=False, encoding='utf-8-sig')


