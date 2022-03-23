"""JJEncode混淆, 最好的方法：浏览器console

1、解密网站解密，解密不完全？？
"""
import os
import re
import requests
from selenium import webdriver

url = 'https://spa10.scrape.center/js/main.js'
response = requests.get(url).text
print(response)

import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


options = webdriver.ChromeOptions()
options.add_argument('--auto-open-devtools-for-tabs')  # 自动打开开发者工具

d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = {'browser': 'ALL'}

driver = webdriver.Chrome(desired_capabilities=d, options=options)
driver.maximize_window()
driver.get(url='https://www.baidu.com/')


# driver.execute_script("console.log('13215356')")

# driver.execute_script("location.reload()")
js = response

js = 'var a =' + js[:-4] + ';'
print(js)
aa = driver.execute_script(js)
print(aa)
# print(driver.get_log("browser"))
time.sleep(15)
driver.close()