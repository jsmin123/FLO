from setting.spread_sheet import *
from setting.function import *
from media.DA.DA_rule import *
import re

def sub_media_data():
    sub_media_data = sub_media_raw_data_read()
    fill_values(sub_media_data, DA_value_columns, 0)
    sub_media_data['노출'] = pd.to_numeric(sub_media_data['노출'])
    sub_media_data['클릭'] = pd.to_numeric(sub_media_data['클릭'])
    sub_media_data['비용'] = pd.to_numeric(sub_media_data['비용'])
    fill_values(sub_media_data, DA_pivot_columns, '')
    sub_media_data = sub_media_data[DA_report_columns]
    return sub_media_data

def remerge(df):
    df = df.loc[df['매체']=='remerge']
    df['광고그룹'] = df['광고']
    df['OS'] = df['캠페인'].apply(lambda x : 'AOS' if 'AND_' in x.upper() else 'iOS' if 'IOS_' in x.upper() else '-')
    df['플랫폼'] = '-'
    return df

def gfa(df):
    df = df.loc[df['매체']=='gfa']
    df['OS'] = df['OS'].apply(lambda x: 'AOS' if x == 'Android' else 'iOS' if x == 'iOS' else x)
    df['캠페인'] = df['OS']
    df['광고그룹'] = ''
    df['광고'] = df['광고'].str.replace(pat='_링크교체\(11\/5\)', repl='')
    return df

def moloco(df):
    df = df.loc[df['매체']=='moloco']
    df['광고'] = df['광고그룹']
    df['OS'] = df['OS'].apply(lambda x: 'AOS' if x == 'ANDROID' else 'iOS' if x == 'IOS' else x)
    df['플랫폼'] = '-'
    return df


def manplus(df):
    data = df.loc[df['매체']=='manplus']
    data['광고'] = data['광고'].apply(lambda x: x[x.find('_', 2) + 1:])
    data['OS'] = data['캠페인']
    data['플랫폼'] = '-'
    return data

def blind(df) :
    df = sub_media_data()
    data = df.loc[df['매체']=='blind']
    pat = re.compile('\(.+\)')
    data['광고'] = data['광고'].apply(lambda x : pat.findall(x)[0][1:-1] if pat.search(x) else x[x.find('_', 2) + 1:])
    data['플랫폼'] = '-'
    return data

def sub_media_preprocess():
    raw_data = sub_media_data()
    media_list = list(raw_data['매체'].unique())

    preprocess_dict = {'remerge': remerge(raw_data),
                       'gfa': gfa(raw_data),
                       'moloco' : moloco(raw_data),
                       'manplus' : manplus(raw_data),
                       'blind' : blind(raw_data)}
    result = pd.DataFrame()
    for media in media_list:
        try :
            data = preprocess_dict[media]
            result = pd.concat([result, data], sort = False)
        except : pass


    return result



