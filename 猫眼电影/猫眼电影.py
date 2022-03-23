import requests
from fake_useragent import UserAgent
from selenium import webdriver
from lxml import etree
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from urllib.parse import unquote, quote

headers = '''
        Accept: */*
        Accept-Encoding: gzip, deflate, br
        Accept-Language: zh-CN,zh;q=0.9
        Connection: keep-alive
        Cookie: __mta=50223769.1641693450960.1641693477938.1641698467486.6; uuid_n_v=v1; uuid=7F5C1AC070EF11EC8E83C97244BA79F359A801BB59B54A6A8F1F217AD46A4224; _csrf=f23ee575f99ee197de4ed2cd6e9d279c512d73a898b5c6404e4078731876e9de; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1641693451; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=17e3c8e12b5c8-0f2b0bb7054926-4303066-1fa400-17e3c8e12b5c8; _lxsdk=7F5C1AC070EF11EC8E83C97244BA79F359A801BB59B54A6A8F1F217AD46A4224; __mta=50223769.1641693450960.1641693466928.1641693477938.5; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1641698522; _lxsdk_s=17e3cc76c5b-e69-e46-cb2%7C%7C33
        sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
        sec-ch-ua-mobile: ?0
        sec-ch-ua-platform: "Windows"
        Sec-Fetch-Dest: empty
        Sec-Fetch-Mode: cors
        Sec-Fetch-Site: same-origin
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36
        X-Requested-With: XMLHttpRequest
'''

# 注意猫眼电影有滑块反爬
def get_headers(header_raw):
    """
    通过原生请求头获取请求头字典
    :param header_raw: {str} 浏览器请求头
    :return: {dict} headers
    """
    return dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')


def first_url():   # """获取首页的电影url"""
    first_url = 'https://www.maoyan.com/films'   # 可以翻页，但默认定位在广州，选择其他城市后url不变
    response = requests.get(url=first_url, headers=get_headers(headers))
    obj = etree.HTML(response.text)
    url_list = obj.xpath('//dl[@class="movie-list"]//div[@class="movie-item film-channel"]')
    url_first_list = []
    print(len(url_list))
    # for url in url_list:
    for url in url_list[0:2]:
        url = 'https://www.maoyan.com' + url.xpath('./a/@href')[0]
        url_first_list.append(url)
        print(url)
    return url_first_list


class Selenium(object):
    def __init__(self, url_list):
        """浏览器配置1"""
        # 实例化一个ChromeOptions对象,需导入 from selenium.webdriver import ChromeOptions
        self.options = webdriver.ChromeOptions()
        # 随机请求头
        self.ua = UserAgent().random
        self.options.add_argument('--user-agent=' + self.ua)

        # 设置日志提示等级
        self.options.add_argument('--log-level=3')

        # 启动时窗口最大化
        # self.options.add_argument('--start-maximized')

        # 关闭浏览器左上方 ’Chrome正在受到自动测试软件控制‘ 的提示
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # url
        self.url_list = url_list
        # self.url = 'https://passport.58.com/login/?path=https://gz.58.com/searchjob/%3Fpts%3D1641557296383'

    def set_options(self):
        # 将配置导入Chrome浏览器
        self.driver = webdriver.Chrome(options=self.options)
        # 更改navigator信息防止被识别出为selenium爬虫
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })"""})

    def open_browser(self, i):
        """打开浏览器"""
        self.driver.get(i)
        print(i)

    def control_browser(self):
        """控制浏览器"""
        pass

    def parse(self):
        # 切换到跳转后的页面
        time.sleep(1)
        # self.driver.switch_to.window(self.driver.window_handles[0])
        aa = self.driver.page_source
        print(aa)

    def close_browser(self):
        """关闭浏览器"""
        self.driver.quit()
        # self.driver.close()

    def main(self):
        self.set_options()
        for i in self.url_list:
            self.open_browser(i)
            time.sleep(2)
            self.parse()
            time.sleep(3)
            self.close_browser()


if __name__ == '__main__':
    try:
        url = first_url()
    except Exception as e:
        pass
    else:
        selenium = Selenium(url)
        selenium.main()
