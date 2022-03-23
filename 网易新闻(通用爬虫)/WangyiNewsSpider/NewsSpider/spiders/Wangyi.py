import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from WangyiNewsSpider.NewsSpider.items import NewsspiderItem


class WangyiSpider(CrawlSpider):
    name = 'Wangyi'
    allowed_domains = ['163.com']
    start_urls = [
                 # 'https://news.163.com/',
                 # 'https://sports.163.com/',
                 'https://sports.163.com/nba/',
        #https://www.163.com/sports/article/H05BIB2B0005877U.html
                 # 'https://ent.163.com/',
                 # 'https://money.163.com/',
                 # 'https://money.163.com/stock/',
                 # 'https://auto.163.com/',
                 # 'https://tech.163.com/',
                 # 'https://mobile.163.com/',
                 # 'https://fashion.163.com/',
                 # 'https://travel.163.com/',
                 # 'https://travel.163.com/',
                 # 'https://home.163.com/',
                 # 'https://edu.163.com/',
                  ]
    # 'https://www.163.com/dy/article/GVUP6FTG0552YKVK.html'
    # https://www.163.com/mobile/article/GVSQB0TE00119821.html
    rules = (
        Rule(LinkExtractor(allow=r'https://www.163.com/sports/.*?html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = NewsspiderItem()
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        item['title'] = response.xpath('//h1[@class="post_title"]/text()').extract_first()
        item['time'] = response.xpath('//div[@class="post_info"]/text()').extract_first().replace('\n', '').strip().replace('\u3000',' ') + response.xpath('//div[@class="post_info"]/a/text()').extract_first()
        content = response.xpath('//div[@class="post_body"]/p/text()').extract()  # list -> str
        item['content'] = ''.join(content)
        return item
