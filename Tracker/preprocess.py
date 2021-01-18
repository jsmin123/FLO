import pandas as pd
import datetime
import re
from setting.directory import *
from setting.report_date import *
from setting.spread_sheet import *
from setting.function import *
from Tracker.tracker_rule import *
from media.DA import *

from media.DA.twitter import twitter_id_table
from media.DA.google_da import google_id_table

def fb(df, source):
    data = df.loc[df['media_source']==source]
    return data

def google(df, source):
    data = df.loc[df['media_source']==source]
    data['광고'] = data['광고그룹']
    return data

def remerge(df,source):
    data = df.loc[df['media_source']==source]
    data['광고'] = data['광고그룹']
    data['플랫폼'] = '-'
    return data

def social_twitter(df, source) :
    data = df.loc[df['media_source']==source]
    data['캠페인'] = data['광고']
    data['광고그룹'] = data['광고']
    data['플랫폼'] = '-'

    apps_index = index_sheet()
    twitter_index = apps_index.loc[apps_index['매체']=='Twitter'][['광고', '광고그룹', '캠페인']]
    twitter_index['media_source']='Social Twitter'
    data = data.drop(['캠페인', '광고그룹'], axis = 1)
    data = data.merge(twitter_index, on = ['media_source', '광고'], how= 'left')
    data['media_source'] = 'Twitter'
    data['플랫폼'] = '-'
    # 트위터 광고 -> 인덱스 시트 활용해서 전부 string 형태 광고명으로 변경할 필요 있음
    return data

def twitter(df, source) :
    data = df.loc[df['media_source']==source]
    data['플랫폼'] = '-'
    return data

def criteo(df, source) :
    data = df.loc[df['media_source']==source]
    data['캠페인'] = data['OS']
    data.loc[data['광고'].str.upper().str.count(pat='ADID') > 0, '캠페인'] = 'ADID'
    data['플랫폼'] = '-'
    return data

def moloco(df, source) :
    data = df.loc[df['media_source']==source]
    data['광고'] = ''
    data['광고그룹'] = ''
    data['플랫폼'] = '-'
    return data

def gfa(df, source) :
    data = df.loc[df['media_source']==source]
    data['플랫폼'] = data['media_source']
    data['캠페인'] = data['OS']
    naver_platform_dict = {'NAVER_main': '모바일 메인',
                           'NAVER_sub': '모바일 서브_배너',
                           'NAVER_smart': '스마트채널'}
    data['플랫폼'] = data['플랫폼'].apply(lambda x: naver_platform_dict.get(x))
    data['광고그룹'] = ''
    data['media_source'] = 'naver_gfa'
    return data

def manplus(df, source):
    data = df.loc[df['media_source']==source]
    data['캠페인'] = data['OS']
    data['플랫폼'] = '-'
    return data

def blind(df, source):
    data = df.loc[df['media_source']==source]
    data['캠페인'] = ''

    da_top = re.compile('_da_top')
    da_bottom = re.compile('_da_bottom')
    da_feed = re.compile('_da_feed')
    platform_list = [da_top, da_bottom, da_feed]
    platform_dict = {da_top: 'TOTAL_띠배너 상단',
                     da_bottom: 'TOTAL_띠배너 하단',
                     da_feed: 'TOTAL_피드광고'}

    def blind_creative(data):
        for pat in platform_list:
            if pat.search(data):
                return pat.sub('', data)
            else:pass
        return data

    def blind_group(data):
        for pat in platform_list:
            if pat.search(data):
                return platform_dict.get(pat)
            else: pass
        return ''

    data['광고'].apply(lambda x: da_feed.search(str(x)))

    data['광고그룹'] = data['광고'].apply(blind_group)
    data['광고'] = data['광고'].apply(blind_creative)
    data['플랫폼'] = '-'
    return data

def apps_da_rawdata():
    apps_raw = pd.read_csv(tracker_raw_dir + f'/apps_{day_1_yearmonth}.csv', low_memory=False)
    apps_raw['OS'] = apps_raw['platform'].apply(lambda x: 'AOS' if x == 'android' else 'iOS' if x == 'ios' else x)
    apps_raw['Touch Date'] = pd.to_datetime(apps_raw['attributed_touch_time']).dt.date
    apps_raw['Install Date'] = pd.to_datetime(apps_raw['install_time']).dt.date
    apps_raw['Event Date'] = pd.to_datetime(apps_raw['event_time']).dt.date

    apps_da_raw = apps_raw[da_columns]
    apps_da_raw = apps_da_raw.loc[apps_da_raw['media_source'].isin(da_media_list)]
    apps_da_raw = apps_da_raw.rename(columns={'Event Date': '날짜',
                                              'channel': '플랫폼',
                                              'campaign': '캠페인',
                                              'adset': '광고그룹',
                                              'ad': '광고'})
    # 테스트용 임시
    apps_da_raw = apps_da_raw.loc[(apps_da_raw['날짜'] <= datetime.date(year=2020, month=12, day=6)) &
                                  (apps_da_raw['날짜'] >= datetime.date(year=2020, month=12, day=1))]

    # 리타게팅 캠페인의 UA 이벤트 필터링
    re_media_ua_events = ((apps_da_raw['media_source'].isin(retargeting_media_list)) & (apps_da_raw['구분'] == 'UA'))
    apps_da_raw = apps_da_raw[~re_media_ua_events]

    google_id = google_id_table()
    google_group_id_dict = media_group_id_dict(google_id)
    twitter_id = twitter_id_table()
    twitter_group_id_dict = media_group_id_dict(twitter_id)

    # 맨플러스 media source 변경
    apps_da_raw.loc[apps_da_raw['media_source']=='manplus', 'media_source'] = 'manplus_int'

    def set_group_id(row):
        x = row['광고그룹']
        if row['media_source'] == 'googleadwords_int':
            if pd.notnull(x): return google_group_id_dict.get(int(x))
        if row['media_source'] == 'Twitter':
            if pd.notnull(x): return twitter_group_id_dict.get(x)
        return x

    # 그룹 ID 매핑
    apps_da_raw['광고그룹'] = apps_da_raw.apply(set_group_id, axis = 1)

    media_list = list(apps_da_raw['media_source'].unique())
    preprocess_dict = {'Facebook Ads' : fb(apps_da_raw, source = 'Facebook Ads'),
                        'googleadwords_int': google(apps_da_raw, source = 'googleadwords_int'),
                       'remerge_int': remerge(apps_da_raw, source = 'remerge_int'),
                       'Social Twitter' : social_twitter(apps_da_raw, source = 'Sorcial Twitter'),
                       'Twitter' : twitter(apps_da_raw, source = 'Twitter'),
                       'criteonew_int' : criteo(apps_da_raw, source = 'criteonew_int'),
                       'moloco_int' : moloco(apps_da_raw, source = 'moloco_int'),
                       'NAVER_main' : gfa(apps_da_raw, source = 'NAVER_main'),
                       'NAVER_sub' : gfa(apps_da_raw, source = 'NAVER_sub'),
                       'NAVER_smart' : gfa(apps_da_raw, source = 'NAVER_smart'),
                       'manplus_int' : manplus(apps_da_raw, source = 'manplus_int'),
                       'blind' : blind(apps_da_raw, source = 'blind')}

    result = pd.DataFrame()
    for media in media_list:
        try :
            data = preprocess_dict[media]
            result = pd.concat([result, data], sort = False)
        except : pass


    # 원링크 관련 전처리

    # 데이터 매핑을 위해 날짜 서식 지정
    result['날짜'] = pd.to_datetime(result['날짜']).dt.date
    return result

def event_table(df, event_name, column_name):
    pivot_columns = ['OS', '날짜', 'media_source', '플랫폼', '캠페인', '광고그룹', '광고']
    temp = df.loc[df['event_name'] == event_name]
    temp['cnt'] = 1
    fill_values(temp, pivot_columns, '')
    temp = temp.pivot_table(index=pivot_columns, values='cnt', aggfunc='sum')
    temp = temp.reset_index()
    temp = temp.rename(columns={'cnt': column_name})
    return temp
