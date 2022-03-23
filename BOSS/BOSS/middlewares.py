import time
from scrapy import signals
from fake_useragent import UserAgent
from itemadapter import is_item, ItemAdapter
import asyncio
import aiohttp
# from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
# from BOSS.selenium_get_cookes import selenium_get_cookie
from scrapy.http import HtmlResponse


class UserAgentMiddleware:
    def process_request(self, request, spider):
        request.headers['User-Agent'] = UserAgent().random
        return None


class SeleniumMiddleware:
    """使用aiohttp异步发起请求获取cookie + selenium无头浏览器模式"""

    # def process_request(self, request, spider):
    #     token = self.get_cookies()
    #     request.cookies = {
    #         '__zp_stoken__': token,
    #     }
    #     return None
    def process_request(self, request, spider):
        # token = selenium_get_cookie()
        # request.cookies = {
        #     '__zp_stoken__': token,
        # }
        # # return None

        url = request.url

        # 设置无头模式
        # 1.创建一个参数对象，用来控制chrome以无界面模式打开
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # chrome_options.add_argument('--disable-gpu')

        # 2.创建浏览器对象
        browser = webdriver.Chrome(options=chrome_options)
        # browser = webdriver.Chrome()
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
        	Object.defineProperty(navigator, 'webdriver', {
        	get: () => undefined
        })"""})
        browser.get(url)
        time.sleep(2)
        html = browser.page_source
        browser.close()
        return HtmlResponse(url=request.url,
                            body=html,
                            request=request,
                            encoding='utf-8',
                            status=200
                            )



