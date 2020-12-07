from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
from setting.directory import *
from setting.auth import *

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



