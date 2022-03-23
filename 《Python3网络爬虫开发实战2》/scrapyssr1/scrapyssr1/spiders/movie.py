import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.loader import ItemLoader
from ..loaders import MovieItemLoader
from scrapyssr1.items import MovieItem


class MovieSpider(CrawlSpider):
    name = 'movie'
    allowed_domains = ['ssr1.scrape.center']
    start_urls = ['http://ssr1.scrape.center/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="el-col el-col-24 el-col-xs-8 el-col-sm-6 el-col-md-4"]/a'), callback='parse_detail', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="number"]/a'))
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item

    def parse_detail(self, response):
        # print(response.url)

        loader = MovieItemLoader(item=MovieItem(), response=response)
        loader.add_xpath('name', '//h2[@class="m-b-sm"]/text()')
        loader.add_xpath('cover', '//img[@class="cover"]/@src')
        loader.add_xpath('categories', '//div[@class="categories"]//span/text()')
        loader.add_xpath('published_at', '//div[@class="m-v-sm info"]/span/text()')
        loader.add_xpath('drama', '//div[@class="drama"]/p/text()')
        loader.add_xpath('score', '//p[@class="score m-t-md m-b-n-sm"]/text()')
        print(loader.load_item())
        yield loader.load_item()


        # item = MovieItem()
        # item['name'] = response.xpath('//h2[@class="m-b-sm"]/text()').extract_first()
        # item['categories'] = response.xpath('//div[@class="categories"]//span/text()').extract()
        # item['cover'] = response.xpath('//img[@class="cover"]/@src').extract_first()
        # item['published'] = response.xpath('//div[@class="m-v-sm info"]/span/text()')
        # item['score'] = response.xpath('//p[@class="score m-t-md m-b-n-sm"]/text()').extract_first().strip()
        # item['drama'] = response.xpath('//div[@class="drama"]/p/text()').extract_first().strip()
        # yield item