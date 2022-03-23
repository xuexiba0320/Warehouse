import time
from lxml import etree
import asyncio
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from selenium import webdriver


def browser_parse(url):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    time.sleep(1)
    html = browser.page_source
    res = etree.HTML(html)
    data_list = []
    items = res.xpath('//div[@class="job-list"]/ul/li')
    for item in items:
        # data = {}
        href = 'https://www.zhipin.com' + item.xpath('.//span[@class="job-name"]/a/@href')[0]
        title = item.xpath('.//span[@class="job-name"]/a/@title')[0]
        area = item.xpath('.//span[@class="job-area"]/text()')[0]
        price = item.xpath('.//div[@class="job-limit clearfix"]/span/text()')[0]
        year = item.xpath('.//div[@class="job-limit clearfix"]/p[2]/text()')
        publisher = item.xpath('.//div[@class="job-limit clearfix"]/div[@class="info-publis"]/h3/text()')[0]
        # data = {
        #     'href': href,
        #     'title': title,
        #     'area': area,
        #     'price': price,
        #     'year': year,
        #     'publisher': publisher,
        #
        # }
        print(href, title, area, price, year, publisher)

        # print(data)
        # data_list.append(data)

    browser.close()
    # return data_list



def run():
    # pool = ThreadPoolExecutor(15)
    with ThreadPoolExecutor(6) as pool:
        # url = f'https://www.zhipin.com/c101280100-p100901/?page={i}&ka=page-{i}'
        urls = [f'https://www.zhipin.com/c101280100-p100901/?page={i}&ka=page-{i}' for i in range(1, 11)]
        result = pool.map(browser_parse, urls)
        # for y in result:
        #     print(y)


if __name__ == '__main__':
    run()