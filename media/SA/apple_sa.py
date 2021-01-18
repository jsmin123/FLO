from setting.auth import *
from setting.directory import *
from setting.report_date import *

import requests
from os import listdir
from os.path import isfile, join
import datetime
import pandas as pd
from pandas import json_normalize
import time

def normalize(res_data):
    df = pd.DataFrame()
    res = res_data['data']['reportingDataResponse']['row']
    for i in range(len(res)):
        if range(len(res)).index(i) == 0:
            df = json_normalize(res_data['data']['reportingDataResponse']['row'][i], 'granularity')
            df['keyword'] = res_data['data']['reportingDataResponse']['row'][i]['metadata']['keyword']
            df['adGroupName'] = res_data['data']['reportingDataResponse']['row'][i]['metadata']['adGroupName']
        else:
            df1 = json_normalize(res_data['data']['reportingDataResponse']['row'][i], 'granularity')
            df1['keyword'] = res_data['data']['reportingDataResponse']['row'][i]['metadata']['keyword']
            df1['adGroupName'] = res_data['data']['reportingDataResponse']['row'][i]['metadata']['adGroupName']
            df = pd.concat([df, df1])
            df = df.reset_index(drop=True)
    return df

def normalize2(res_data):
    df = pd.DataFrame()
    res2 = res_data['data']['reportingDataResponse']['row']
    for i in range(len(res2)):
        if range(len(res2)).index(i) == 0:
            df = json_normalize(res_data['data']['reportingDataResponse']['row'][i], 'granularity')
            df['keyword'] = res_data['data']['reportingDataResponse']['row'][i]['metadata']['searchTermText']
            df['adGroupName'] = res_data['data']['reportingDataResponse']['row'][i]['metadata']['adGroupName']
        else:
            df1 = json_normalize(res_data['data']['reportingDataResponse']['row'][i], 'granularity')
            df1['keyword'] = res_data['data']['reportingDataResponse']['row'][i]['metadata']['searchTermText']
            df1['adGroupName'] = res_data['data']['reportingDataResponse']['row'][i]['metadata']['adGroupName']
            df = pd.concat([df, df1])
            df = df.reset_index(drop=True)
    return df

def asa_report(Sdate, Edate):
    report = {
        "startTime": Sdate,
        "endTime": Edate,
        "granularity": "DAILY",
        "selector": {
            "orderBy": [
                {
                    "field": "adGroupId",
                    "sortOrder": "DESCENDING"
                }
            ], "fields": [
                "localSpend", "taps"
            ],
            "conditions": [
            ],
            "pagination": {
                "offset": 0,
                "limit": 1000
            }
        },
        "timeZone": "ORTZ",
        "returnRecordsWithNoMetrics": False,
        "returnRowTotals": False,
        "returnGrandTotals": False
    }

    return report

def asa_res_json(url, headers, certificate_path, certificate_key_path, s_date, e_date):
    while True:
        try:
            response = requests.post(url, cert=(certificate_path, certificate_key_path),
                                     json=asa_report(s_date, e_date), headers=headers)
            res = response.json()
        except:
            time.sleep(10)
            print('서버 호출 에러로 10초 후 다시 실행합니다')
            continue
        break
    return res

def res_to_df(res, key, norm_type=1):
    if (norm_type == 1) | (norm_type == 2):
        pass
    else:
        raise ValueError()

    try:
        if norm_type == 1:
            res_df = normalize(res)
        elif norm_type == 2:
            res_df = normalize2(res)
    except:
        res_df = pd.DataFrame(
            columns=['date', 'campaign', 'adGroupName', 'keyword', 'impressions', 'taps', 'localSpend.amount'])
    res_df['campaign'] = key

    return res_df

def apple_sa_load():
    headers = {"Authorization": "orgId=%s" % org_id, 'Content-Type': 'application/json'}

    url = 'https://api.searchads.apple.com/api/v3/campaigns'
    response = requests.get(url, cert=(certificate_path, certificate_key_path), headers=headers)
    res = response.json()
    camp_id = {}

    apple_sa_dir = sa_raw_dir + '/apple_sa/raw_data'

    for x in range(len(res["data"])):
        camp_id.update({(res["data"][x]["name"]): (res["data"][x]["id"])})

    files = [f for f in listdir(apple_sa_dir) if
             isfile(join(apple_sa_dir, f))]

    day = start_day
    monthly_data = pd.DataFrame()

    while day < today:
        file_name = 'apple_sa_raw_{}.csv'.format(day.strftime('%Y-%m-%d'))

        if file_name in files:
            daily_data = pd.read_csv(apple_sa_dir + '/' + file_name)
            print(f'{day} 일자의 Raw Data가 이미 존재합니다.')

        else:
            daily_data = pd.DataFrame()
            s_date = day.strftime('%Y-%m-%d')
            e_date = day.strftime('%Y-%m-%d')

            for index, (key, value) in enumerate(camp_id.items()):
                if "SearchMatch" not in key:
                    url = f'https://api.searchads.apple.com/api/v3/reports/campaigns/{value}/keywords'
                    res = asa_res_json(url, headers, certificate_path, certificate_key_path, s_date, e_date)
                    res_df = res_to_df(res, key, norm_type=1)
                    daily_data = pd.concat([daily_data, res_df], sort = False)

                else:
                    url = f'https://api.searchads.apple.com/api/v3/reports/campaigns/{value}/searchterms'
                    res = asa_res_json(url, headers, certificate_path, certificate_key_path, s_date, e_date)
                    res_df = res_to_df(res, key, norm_type=2)
                    daily_data = pd.concat([daily_data, res_df], sort = False)

            daily_data = daily_data.reset_index(drop=True)

            try:
                daily_data = daily_data[
                    ['date', 'campaign', 'adGroupName', 'keyword', 'impressions', 'taps', 'localSpend.amount']]
            except:
                daily_data = pd.DataFrame(
                    columns=['date', 'campaign', 'adGroupName', 'keyword', 'impressions', 'taps',
                             'localSpend.amount'])
            daily_data.to_csv(apple_sa_dir + '/' + file_name, encoding='utf-8-sig',
                              index=False)
            print(f'{day} 일자의 Raw Data를 적재하였습니다.')

        monthly_data = pd.concat([monthly_data, daily_data], sort=False)
        day = day + datetime.timedelta(1)

    monthly_data.to_csv(
        sa_raw_dir + f'/apple_sa/apple_sa_{day_1_yearmonth}.csv',
        encoding='utf-8-sig', index=False)

    print('---')
    print('Apple Search Ads {}월 통합 Raw Data 적재 완료하였습니다.'.format(day_1.month))

#
# def apple_sa_preprocess():
#     apple_sa_raw = common.media_month_data_read('apple_sa', ReportDate.day_1_yearmonth())
#
#     apple_sa_raw = apple_sa_raw.rename(columns=
#     {
#         'date': '날짜',
#         'campaign': '캠페인',
#         'adGroupName': '광고그룹',
#         'keyword': 'term',
#         'impressions': '노출',
#         'taps': '클릭',
#         'localSpend.amount': '비용'
#     })
#
#     apple_sa_raw['디바이스'] = 'iOS'
#     apple_sa_raw['매체'] = 'Apple_SA'
#     apple_sa_raw['term'] = apple_sa_raw['term'].fillna('알수없음')
#
#     apple_sa = apple_sa_raw.merge(SA.SA_rule.sa_index, on='캠페인', how='left')
#
#     common.fill_values(apple_sa, columns=['기획전명', '상품구분', '소재'], fill_type='')
#     common.fill_values(apple_sa, columns=['구매(1일)', '구매(7일)', '매출(1일)', '매출(7일)', '발송', '조회'], fill_type=0)
#
#     common.str_to_numeric(apple_sa, ['노출', '클릭'], typ='int')
#     common.str_to_numeric(apple_sa, ['비용'], typ='float')
#
#     apple_sa['source'] = 'apple.searchads'
#     apple_sa_data = apple_sa.copy()
#     return apple_sa_data
