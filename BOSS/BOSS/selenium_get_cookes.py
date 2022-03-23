from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
import time


def selenium_get_cookie():
    url = 'https://www.zhipin.com/job_detail/?query=%E5%89%8D%E7%AB%AF&city=101280100&industry=&position='
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--headless')

    browser = webdriver.Chrome(options=options)
    browser.get(url=url)
    time.sleep(2)
    cookies = browser.get_cookies()
    # cookie 处理 --> 取出__token_的对应的值
    for cookie in cookies:
        if cookie['name'] == '__zp_stoken__':
            print('最新cookie值为:', cookie['value'])
            return cookie['value']  # 退出函数

