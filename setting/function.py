import pandas as pd
from setting.directory import *
from setting.auth import *
from setting.report_date import *
import requests
import datetime
import re

def media_raw_read(media):
    file_name = media_raw_dir + f'/{media}/{media}_{day_1_yearmonth}.csv'
    raw_data = pd.read_csv(file_name)
    return raw_data


def exchange_rate(date):
    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
    params = {'authkey' : open_api_key,
              'searchdate' : date,
              'data' : 'AP01'}

    res = requests.get(url = url, params = params)
    data = res.json()
    today_rate = 0

    if len(data) > 0 :
        columns = list(data[0].keys())
        rate_table = pd.DataFrame(columns = columns)
        for i in range(0,len(data)):
            for col in columns :
                rate_table.loc[i,col] = data[i][col]
        today_rate = rate_table.loc[rate_table['cur_unit'] == 'USD', 'deal_bas_r'].values[0]
    else : today_rate=0

    return today_rate

def exchange_rate_update() :
    df = pd.read_csv(report_dir + '/usd_exchange_rate.csv')
    max_date = datetime.datetime.strptime(df['날짜'].max(), '%Y-%m-%d').date()

    if max_date!=day_1:
        day = max_date + datetime.timedelta(1)
        while day <= day_1 :
            day_text = day.strftime('%Y-%m-%d')
            rate = exchange_rate(day_text)
            report_rate = rate

            if report_rate==0:
                business_day = df.loc[df['환율']!=0]
                last_date = business_day['날짜'].max()
                report_rate = df.loc[df['날짜']==last_date, '적용환율'].values[0]

            df = df.append({'날짜': day_text, '환율': rate, '적용환율' : report_rate}, ignore_index=True)
            day = day + datetime.timedelta(1)
            print(f'{day} 일자 환율 정보를 업데이트 하였습니다.')

    else :
        print('이미 환율 데이터가 최신 상태입니다.')

    df.to_csv(report_dir + '/usd_exchange_rate.csv', index = False, encoding = 'utf-8-sig')

# Raw Data 다운로드 여부 확인
def date_checker(files, day = start_day):
    file_date = []
    date_pat = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')
    for f in files:
        parse_date = date_pat.findall(f)[0]
        file_date.append(parse_date)

    result = []
    while day < today:
        day_str = day.strftime('%Y-%m-%d')
        if day_str not in file_date:
            result.append(day_str)

        day += datetime.timedelta(1)

    return result

# columns에 있는 nan값들을 fill_type으로 채움
def fill_values(df, columns, fill_type):
    for col in columns:
        if col not in df.columns:
            df[col] = fill_type
        df[col] = df[col].fillna(fill_type)

def monthly_data_read(campaign,name):
    dir = media_raw_dir + '/' + campaign + '/' + name
    file_name = f'/{name}_{day_1_yearmonth}.csv'
    data = pd.read_csv(dir + '/' + file_name, low_memory = False)
    print(f'{name} 파일 Read 완료')
    return data

def media_group_id_dict(df):
    group_id = df[['광고그룹 ID', '광고그룹']]
    group_id = group_id.set_index('광고그룹 ID')
    group_id_dict = group_id.to_dict()['광고그룹']
    return group_id_dict




