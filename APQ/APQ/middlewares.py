# coding=utf-8
# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
import time

import APQ.settings
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver


# useful for handling different item types with a single interface


# class SeleniumMiddleware(object):
#
#     def process_request(self, request, spider):
#         url = request.url
#         print(url)
#
#         print('nihoa hghajd4444')
#         driver = webdriver.Chrome()
#         driver.get(url)
#         if 'daydata' in url:
#             driver = webdriver.Chrome()
#             driver.get(url)
#             time.sleep(3)
#             data = driver.page_source
#             driver.close()
#             # 创建响应对象
#             res = HtmlResponse(url=url, body=data, encoding='utf-8', request=request)
#             return res


class ApqSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ApqDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        ua = random.choice(APQ.settings.USER_AGENTS_LIST)
        # print(ua)
        request.headers['User-Agent'] = ua
        url = request.url

        if 'daydata' in url:
            # 下面三行是解决（忽略）驱动报错
            # options = webdriver.ChromeOptions()
            # options.add_argument('--log-level=3')
            # driver = webdriver.Chrome(options=options)

            ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) \
            AppleWebKit/602.1.50 (KHTML, like Gecko) Mobile/14A403 \
            MicroMessenger/6.3.27 NetType/WIFI Language/zh_CN'
            options = webdriver.ChromeOptions()
            options.add_argument('user-agent=' + ua)
            options.add_argument('--log-level=3')
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            driver = webdriver.Chrome(options=options)
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
              """
            })

            driver.get(url)
            time.sleep(3)
            data = driver.page_source
            # with open("git222.html", "w")as f:
            #     f.write(data.body.decode('gbk', 'ignore'))
            # print(data)
            # driver.close()
            # 创建响应对象
            # with open('text111.html', 'wb')as  f:
            #     f.write(data.encode())
            res = HtmlResponse(url=url, body=data, encoding='utf-8', request=request)
            return res

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
