from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
from setting.directory import *
from setting.auth import *
from setting.report_date import *

def spread_document_read(spread_url):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    json_file = token_dir + '/' + json_file_name
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    gc = gspread.authorize(credentials)
    read = gc.open_by_url(spread_url)
    print('스프레드시트 읽기 완료')
    return read

spread_url = 'https://docs.google.com/spreadsheets/d/1RieC5yXi8KimlBE7RqvngnuReDQ0-3ryRwEVsxzDgdI/edit#gid=0'
doc = spread_document_read(spread_url)

def spread_sheet(doc, sheet_name, col_num):
    data_sheet = doc.worksheet(sheet_name)
    data_sheet_read = data_sheet.get_all_values()
    result = pd.DataFrame(data_sheet_read, columns=data_sheet_read[col_num]).iloc[col_num + 1:]
    return result

def index_sheet():
    index = spread_sheet(doc, sheet_name = 'INDEX', col_num = 0)
    return index

def naver_bs_sheet():
    sheet = spread_sheet(doc, sheet_name = 'Naver BS', col_num = 0)
    return sheet

def sub_media_raw_data_read():
    dashboard = spread_sheet(doc,sheet_name='매체별 RD ▶', col_num = 0)
    operating_media = dashboard.loc[dashboard[day_1_yearmonth]=='TRUE', '매체'].tolist()

    result = pd.DataFrame()
    for media in operating_media :
        data = spread_sheet(doc, media, 0)
        data = data.loc[pd.notnull(data['날짜'])]
        data = data.loc[pd.to_datetime(data['날짜']).dt.month==day_1.month]
        data['매체'] = media
        result = pd.concat([result, data], sort= False)

    return result




