import selenium.webdriver.common.alert
import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
from setting.selenium_media import *
from setting.spread_sheet import *
from setting.function import *

def bs_download_index():
    files = [f for f in listdir(bs_raw_dir + '/naver_bs/keyword_data') if
             isfile(join(bs_raw_dir + '/naver_bs/keyword_data', f))]
    date_check = date_checker(files)

    if len(date_check) == 0:
        print('이미 모든 Raw Data가 적재되어 있습니다.')
        raise ValueError

    min_date = min(date_check)
    max_date = max(date_check)

    bs_sheet = naver_bs_sheet()
    bs_sheet['총예산'] = pd.to_numeric(bs_sheet['총예산'])
    bs_sheet['Days'] = pd.to_numeric(bs_sheet['Days'])
    bs_sheet['일예산'] = bs_sheet['총예산'] / bs_sheet['Days']

    download_list = bs_sheet.loc[((bs_sheet['시작일'] <= min_date) & (bs_sheet['종료일'] >= min_date)) |
                              ((bs_sheet['시작일'] <= max_date) & (bs_sheet['종료일'] >= max_date))]
    return download_list


def bs_report_download(key_list, camp_list):
    cnt = 0
    for key in tqdm(key_list):
        driver = webdriver.Chrome(chrome_driver, options=option())
        driver.maximize_window()
        # wait = webdriver.support.ui.WebDriverWait(driver, 5)
        driver.get("https://report.da.naver.com/directcode/login.nhn?saveId=true")
        driver.implicitly_wait(5)

        while True:
            try:
                driver.find_element_by_id('idInput').send_keys(key)
            except:
                time.sleep(3)
                driver.get("https://report.da.naver.com/directcode/login.nhn?saveId=true")
                continue
            break

        num = 1
        selenium_click(driver, '//*[@id="submit_btn"]')
        selenium_click(driver, f'//*[@id="mainTable"]/tbody/tr[{num}]/td[2]/a')

        popup = webdriver.common.alert.Alert(driver)
        try:
            popup.accept()
        except:
            pass
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[1])

        # 키워드 데이터 다운로드
        selenium_click(driver, '//*[@id="aside"]/div[2]/div[1]/a/h3')
        selenium_click(driver, '//*[@id="selectorBox"]/div/div/div[1]/ul/li[7]/a')
        selenium_click(driver, '//*[@id="selectorDialog"]/div/div[2]/button[1]')
        time.sleep(3)
        selenium_click(driver, '//*[@id="content"]/div[1]/div[2]/div/ul/li[3]')  # 엑셀다운
        time.sleep(3)
        os.rename(download_dir + '/일별리포트_로그인키 사용자.csv', download_dir + f'/{key}_keyword.csv')

        # 플랫폼 데이터 다운로드
        selenium_click(driver, '//*[@id="aside"]/div[2]/div[1]/a/h3')
        selenium_click(driver, '//*[@id="selectorBox"]/div/div/div[1]/ul/li[7]/a')
        selenium_click(driver, '//*[@id="selectorBox"]/div/div/div[1]/ul/li[8]/a')
        selenium_click(driver, '//*[@id="selectorDialog"]/div/div[2]/button[1]')
        time.sleep(3)
        selenium_click(driver, '//*[@id="content"]/div[1]/div[2]/div/ul/li[3]')  # 엑셀다운
        time.sleep(3)
        os.rename(download_dir + '/일별리포트_로그인키 사용자.csv', download_dir + f'/{key}_platform.csv')

        driver.quit()
        print(f'{cnt + 1}번째 캠페인 Raw Data 다운로드 완료하였습니다. (캠페인 : {camp_list[cnt]})')
        cnt += 1
    print('네이버 브랜드 검색 Raw Data 다운로드 완료')

def naver_bs_load(key_list, camp_list, name):
    raw_dir = bs_raw_dir + f'/naver_bs/{name}_data'

    data = pd.DataFrame()
    for idx, key in enumerate(key_list):
        temp = pd.read_csv(download_dir + f'/{key}_{name}.csv', header=5, encoding='cp949')
        temp['캠페인'] = camp_list[idx]
        temp['공유Key'] = key
        data = pd.concat([data, temp], sort=False)
        os.remove(download_dir + f'/{key}_{name}.csv')
    #data.to_csv(bs_raw_dir + f'/naver_bs/{name}_data/naver_bs_{name}_{day_1_yearmonth}.csv', index = False, encoding = 'utf-8-sig')

    bs_data = data.copy()
    try : bs_data['일자'] = pd.to_datetime(bs_data['일자'], format='%Y.%m.%d.').dt.date
    except : bs_data['일자'] = pd.to_datetime(bs_data['일자']).dt.date

    files = [f for f in listdir(raw_dir) if
             isfile(join(raw_dir, f))]
    date_check = date_checker(files)

    day = start_day
    monthly_data = pd.DataFrame()
    while day < today:
        file_name = f'naver_bs_{name}_{day}.csv'
        day_str = day.strftime('%Y-%m-%d')
        if day_str not in date_check:
            print(f'{day} 일자의 Raw Data가 이미 존재합니다.')
            daily_data = pd.read_csv(raw_dir + '/' + file_name)
        else:
            print(f'{day} 일자의 Raw Data를 추출합니다.')
            daily_data = bs_data.loc[bs_data['일자'] == day]
            daily_data.to_csv(raw_dir + '/' + file_name,encoding='utf-8-sig', index=False)

        monthly_data = pd.concat([daily_data, monthly_data], sort=False)
        day += datetime.timedelta(1)

    print(f'{day_1.month}월 통합 데이터 적재하였습니다.')
    monthly_data.to_csv(bs_raw_dir + f'/naver_bs/naver_bs_{name}_{day_1_yearmonth}.csv',
                        encoding='utf-8-sig', index=False)

# # Raw Data 정제
# def bs_raw_data_export(bs_data):
#     files = [f for f in listdir(directory.media_raw_dir + '/naver_bs/daily_data') if
#              isfile(join(directory.media_raw_dir + '/naver_bs/daily_data', f))]
#     date_check = date_checker(files)
#
#     today = report_date.today
#     day = report_date.ReportDate.start_day()
#     day_1 = report_date.ReportDate.day_1()
#     day_1_yearmonth = report_date.ReportDate.day_1_yearmonth()
#     monthly_data = pd.DataFrame()
#
#     while day < today:
#         file_name = f'naver_bs_raw_{day}.csv'
#
#         day_str = day.strftime('%Y-%m-%d')
#
#         if day_str not in date_check:
#             print(f'{day} 일자의 Raw Data가 이미 존재합니다.')
#             daily_data = pd.read_csv(directory.media_raw_dir + f'/naver_bs/daily_data/{file_name}')
#         else:
#             print(f'{day} 일자의 Raw Data를 추출합니다.')
#             daily_data = bs_data.loc[bs_data['날짜'] == day]
#             daily_data.to_csv(directory.media_raw_dir + f'/naver_bs/daily_data/{file_name}',
#                               encoding='utf-8-sig', index=False)
#
#         monthly_data = pd.concat([daily_data, monthly_data], sort=False)
#         day += datetime.timedelta(1)
#
#     print(f'{day_1.month}월 통합 데이터 적재하였습니다.')
#     monthly_data.to_csv(directory.media_raw_dir + f'/naver_bs/naver_bs_{day_1_yearmonth}.csv',
#                         encoding='utf-8-sig', index=False)