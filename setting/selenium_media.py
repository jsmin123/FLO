from setting.function import *
from setting.report_date import *
import time
from selenium import webdriver
import re

# 웹사이트 지연에 의해 XPATH를 클릭하지 못할 경우, 성공할때 까지 시도
def selenium_click(driver, path):
    stat = 0
    while stat == 0:
        try:
            driver.find_element_by_xpath(path).click()
        except:
            print('버튼을 클릭하는데 실패하였습니다. 잠시 후 다시 시도합니다')
            time.sleep(2)
            continue

        stat = 1

# 셀레니움용 sleep 간편 함수(간편하게 사용하기 위해 미리 지정)
def slp(sleep_time=5):
    time.sleep(sleep_time)


def option():
    options = webdriver.ChromeOptions()

    # 브라우저 윈도우 사이즈
    options.add_argument('window-size=1920x1080')

    # headless 옵션 설정
    # options.add_argument('headless')
    # options.add_argument("no-sandbox")

    # 사람처럼 보이게 하는 옵션들
    options.add_argument("disable-gpu")  # 가속 사용 x
    options.add_argument("lang=ko_KR")  # 가짜 플러그인 탑재
    options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정
    return options



