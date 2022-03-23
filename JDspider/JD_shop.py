"""
京东华为官方旗舰店商品信息爬取
PS：由于不同的页面结构不同，现在就只针对首页出现的商品进行爬取
待增加功能：评论信息获取（有API接口可以使用）
待尝试改进:多线程or多进程，大数据爬取未进行验证会被封号
"""
import requests
from lxml import etree
from fake_useragent import UserAgent
import json


class JDShop(object):
    def __init__(self):
        self.URL = 'https://mall.jd.com/index-1000004259.html?from=pc'
        useragent = UserAgent()
        UA = useragent.random
        self.headers = {
            'user-agent': UA
        }
        self.goods_url_list = []

    def re_url(self):
        """Enter the home page to obtain product information(goods url)"""
        response = requests.get(url=self.URL, headers=self.headers).text
        xpath_obj = etree.HTML(response)
        page_data = xpath_obj.xpath('//div[@class="layout-main"]/div')
        print(len(page_data))
        for data in page_data:
            goods = data.xpath('./div//div[@class="d-hotSpot"]/div[@class="d-content J_htmlContent"]/a/@href')

            """ filtration data """
            if len(goods):
                for i in goods:
                    if i.startswith('//item.jd.com'):
                        url = 'https:' + i
                        self.goods_url_list.append(url)

        print(len(self.goods_url_list))

    def detail_page(self):
        """get goods information"""
        print(self.goods_url_list)
        for url in self.goods_url_list:
            response = requests.get(url=url, headers=self.headers).text
            # print(response)
            self.parse(response, url)

    def parse(self,response, url):
        """parse title,price"""
        xpath_obj = etree.HTML(response)
        # Determine if the 'img' exists
        try:
            if xpath_obj.xpath('//div[@class="sku-name"]/img'):
                title = xpath_obj.xpath('//div[@class="sku-name"]/text()')[1].strip()
            else:
                title = xpath_obj.xpath('//div[@class="sku-name"]/text()')[0].strip()
        except Exception as result:
            title = 'null'
        # Prices are loaded via Ajax
        goods_id = url.rsplit('/', 1)[1].split('.')[0]
        price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(goods_id)
        # tip:if no headers in here, unable to get data
        price = requests.get(url=price_url, headers=self.headers)
        price = (json.loads(price.text))[0]['p']
        link = url

        self.save(title, price, link)

    @staticmethod
    def save(title, price, link):
        """save data"""
        print(title, price, link)

    def main(self):
        """main function"""
        self.re_url()
        self.detail_page()


if __name__ == '__main__':
    """start project"""
    JDShop = JDShop()
    JDShop.main()
