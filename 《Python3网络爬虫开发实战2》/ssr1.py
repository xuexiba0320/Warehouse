import requests
import re
import logging
from urllib.parse import urljoin
from lxml import etree
import json
from os import makedirs
from os.path import exists


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')  # 定义日志输出级别和输出格式
base_url = 'https://ssr1.scrape.center'
total_page = 10


def scrape_page(url):
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url=url)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)

def scrape_index(page):
    index_url = f"{base_url}/page/{page}"
    return scrape_page(index_url)

def parse_index(html):
    xpath_obj = etree.HTML(html)
    items = xpath_obj.xpath('//a[@class="name"]/@href')
    if not items:
        return []
    for item in items:
        detail_url = urljoin(base_url, item)
        logging.info('get detail url %s', detail_url)
        yield detail_url

def scrape_detail(url):
    return scrape_page(url)

def parse_detail(html):
    detail_xpath = etree.HTML(html)

    name = detail_xpath.xpath('//h2[@class="m-b-sm"]/text()')
    # print(name)
    return name

RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

def save_data(data):
    name = data[0]
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'),ensure_ascii=False, indent=2)

def main():
    data_list = []
    for page in range(1, total_page+1):
        index_html = scrape_index(page)
        detail_urls = parse_index(index_html)
        data_list.append(detail_urls)
        # logging.info('detail urls %s', detail_urls)
        # print(data_list)
        for detail_url in detail_urls:
            detail_html = scrape_detail(detail_url)
            data = parse_detail(detail_html)
            save_data(data)
            logging.info('get detail data %s', data)


if __name__ == '__main__':
    main()