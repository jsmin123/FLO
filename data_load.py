from media import *
from setting.function import *

if __name__ == '__main__' :
    # 네이버 브검 다운로드용 인덱스
    download_index = BS.naver_bs.bs_download_index()
    key_list = download_index['공유Key'].to_list()
    camp_list = download_index['캠페인'].to_list()
    # 셀레니움
    BS.naver_bs.bs_report_download(key_list, camp_list)
    BS.naver_bs.naver_bs_load(key_list, camp_list, 'keyword')
    BS.naver_bs.naver_bs_load(key_list, camp_list, 'platform')
    print('BS 데이터 적재 완료')

    # 트래커 데이터 적재

    # SA 데이터 적재
    SA.apple_sa.apple_sa_load()
    SA.naver_sa.naver_sa_load()
    SA.google_sa.google_sa_load()
    print('SA 데이터 적재 완료')

    # DA 데이터 적재
    DA.facebook.facebook_load()
    DA.google_da.google_da_load()
    print('DA 데이터 적재 완료')

    # 환율 업데이트트
    exchange_rate_update()