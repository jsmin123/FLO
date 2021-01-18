# 개인 로컬 환경에 맞추어 조정
dropbox_dir = 'C:/Dropbox'
download_dir = 'C:/Users/asdad/Downloads'
# ========================

report_dir = dropbox_dir + '/광고 영업/2. 광고주/FLO/자동화 리포트'
env_dir = dropbox_dir + '/광고 영업/2. 광고주/FLO/Report Automation'

media_raw_dir = report_dir + '/1. 매체 데이터'
da_raw_dir = media_raw_dir + '/DA'
sa_raw_dir = media_raw_dir + '/SA'
bs_raw_dir = media_raw_dir + '/BS'

tracker_raw_dir = report_dir + '/2. 트래커 데이터'
ua_raw_dir = tracker_raw_dir + '/UA'
re_raw_dir = tracker_raw_dir + '/RE'

merge_raw_dir = report_dir + '/3. 머지 데이터'
token_dir = env_dir + '/token'

#셀레니움용 크롬드라이버
chrome_driver = token_dir + '/chromedriver'