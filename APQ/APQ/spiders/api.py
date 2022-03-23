import scrapy
from APQ.items import ApqItem


class ApiSpider(scrapy.Spider):
    name = 'api'
    allowed_domains = ['aqistudy.cn']
    start_urls = ['https://www.aqistudy.cn/historydata/']

    def parse(self, response):
        url_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div/li/a/@href').extract()
        print(len(url_list))

        for url in url_list[10:11]:
            # 完整的URL拼接URLjoin

            city_url = response.urljoin(url)
            # print(city_url)
            # 发起对该城市详情页面的请求
            yield scrapy.Request(
                url=city_url,
                callback=self.parse_month
            )

    def parse_month(self, response):
        url_list_month = response.xpath('//*[@id="body"]/div[3]/div[1]/div[2]/div[2]/div[2]/ul/li/a/@href').extract()
        # print(len(url_list_month))

        for url in url_list_month[30:31]:
            city_month_url = response.urljoin(url)
            print(city_month_url)

            yield scrapy.Request(
                url=city_month_url,
                callback=self.parse_day
            )

    def parse_day(self, response):
        # 获取所有的数据节点
        node_list = response.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr')
        print('********************************************')
        # 拿到tr节点列表，删除第一个不相关数据
        # del node_list[0]
        city = response.xpath('//div[@class="panel-heading"]/h3/text()').extract_first().split('2')[0]
        # 遍历数据节点列表
        for node in node_list:
            # 创建存储数据的item容器
            item = ApqItem()

            # 先填写一些固定参数
            # item['city'] = city
            # item['url'] = response.url
            # item['timestamp'] = time.time()

            # 提取数据
            item['date'] = node.xpath('./td[3]/text()').extract_first()
            # item['AQI'] = node.xpath('./td[4]/text()').extract_first()
            # item['LEVEL'] = node.xpath('./td/span/text()').extract_first()
            # item['PM2_5'] = node.xpath('./td[8]/text()').extract_first()
            # item['PM10'] = node.xpath('./td[9]/text()').extract_first()
            # item['NO2'] = node.xpath('./td[12]/text()').extract_first()
            # item['CO'] = node.xpath('./td[13]/text()').extract_first()
            # item['SO2'] = node.xpath('./td[14]/text()').extract_first()
            # item['O3'] = node.xpath('./td[16]/text()').extract_first()
            # for k, v in item.items():
            #     print(k, v)

            # 将数据返回给引擎
            yield item
