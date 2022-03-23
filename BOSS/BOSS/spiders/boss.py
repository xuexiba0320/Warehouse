import scrapy
from gerapy_selenium import SeleniumRequest

class BossSpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['www.zhipin.com']

    BASE_URL = 'https://www.zhipin.com'
    CITY = '100010000'  # 全国城市 代号
    KEYWOED = 'python爬虫'
    PAGE_NUM = 5
    # cookies = {
    #     '__zp_stoken__': selenium_get_cookie()
    # }

    def start_requests(self):
        # print(self.cookies)
        for page in range(1, self.PAGE_NUM + 1):
            # 'https://www.zhipin.com/c101280100/?query=python%E7%88%AC%E8%99%AB&page=2&ka=page-2'
            url = f'{self.BASE_URL}/c{self.CITY}/?query={self.KEYWOED}&page={page}&ka=page-{page}'
            yield SeleniumRequest(url=url, callback=self.parse_index)

    def parse_index(self, response):
        print(response.url)
        data_list = response.xpath('//span[@class="job-name"]/a/@href')
        print(len(data_list))
        for data in data_list:
            # 遍历URL集合保存数据到列表中
            data = 'https://www.zhipin.com'+data.get()
            print(data)

    def parse(self, response):
        pass
