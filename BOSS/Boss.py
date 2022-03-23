import time
from lxml import etree
import requests
import re
from selenium import webdriver


def browser_parse(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    time.sleep(1)
    html = browser.page_source
    res = etree.HTML(html)

    items = res.xpath('//div[@class="job-list"]/ul/li')
    for item in items:
        href = 'https://www.zhipin.com' + item.xpath('.//span[@class="job-name"]/a/@href')[0]
        title = item.xpath('.//span[@class="job-name"]/a/@title')[0]
        area = item.xpath('.//span[@class="job-area"]/text()')[0]
        price = item.xpath('.//div[@class="job-limit clearfix"]/span/text()')[0]
        year = item.xpath('.//div[@class="job-limit clearfix"]/p[2]/text()')
        publisher = item.xpath('.//div[@class="job-limit clearfix"]/div[@class="info-publis"]/h3/text()')[0]
        print(href, title, area, price,publisher)

    time.sleep(2)
    browser.close()


def run():
    for i in range(1, 10):
        url = f'https://www.zhipin.com/c101280100-p100901/?page={i}&ka=page-{i}'
        print(f'第{i}页')
        browser_parse(url)


if __name__ == '__main__':
    run()