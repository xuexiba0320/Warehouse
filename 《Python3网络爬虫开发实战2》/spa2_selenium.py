from selenium import webdriver
from selenium.common.exceptions import TimeoutException             # 异常
from selenium.webdriver.common.by import By                         # 元素定位
from selenium.webdriver.support import expected_conditions as EC    # 元素等待
from selenium.webdriver.support.wait import WebDriverWait           # 元素显性等待
from urllib.parse import urljoin




class Spa2_Selenium(object):
    def __init__(self):
        self.base_url = 'https://spa2.scrape.center/'  # https://spa2.scrape.center/page/3
        self.browser = webdriver.Chrome()
        self.browser.get(self.base_url)
        self.wait = WebDriverWait(self.browser, 20)

    def request(self, url, condition, locator):
        try:
            self.browser.get(url)
            self.wait.until(condition(locator))
        except TimeoutException:
            print('出错:', url)

    def index_page(self, page):
        url = f'{self.base_url}page/{page}'
        self.request(url, EC.visibility_of_element_located, (By.CSS_SELECTOR, '#index .item'))
        detail_urls = self.browser.find_elements(By.XPATH, '//a[@class="name"]')
        for i in detail_urls:
            url = i.get_attribute('href')
            detail_url = urljoin(self.base_url, url)
            yield detail_url

    def detail_page(self, detail_url):
        self.request(detail_url, condition=EC.visibility_of_element_located,
                locator=(By.TAG_NAME, 'h2'))
        # name = self.browser.find_element(By.XPATH, '//h2[@class="m-b-sm"]/text()')
        name = self.browser.find_element(By.TAG_NAME, 'h2').text
        print(name)

    def main(self):
        page = 5
        try:
            # 获取详情页url
            for PAGE in range(1, page + 1):
                detail_urls = self.index_page(PAGE)

                for detail_url in list(detail_urls):
                    self.detail_page(detail_url)
                    # print(detail_url)
        except Exception as E:
            print(E)
        finally:
            self.browser.close()


if __name__ == '__main__':
    Spa2_Selenium().main()


# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# import logging
# from urllib.parse import urljoin
# from os import makedirs
# from os.path import exists
# import json
#
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s: %(message)s')
#
# INDEX_URL = 'https://spa2.scrape.center/page/{page}'
# TIMEOUT = 10
# TOTAL_PAGE = 10
# RESULTS_DIR = 'results'
#
# exists(RESULTS_DIR) or makedirs(RESULTS_DIR)
#
# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# options.add_experimental_option('useAutomationExtension', False)
#
# browser = webdriver.Chrome(options=options)
# wait = WebDriverWait(browser, TIMEOUT)
#
#
# def scrape_page(url, condition, locator):
#     logging.info('scraping %s', url)
#     try:
#         browser.get(url)
#         wait.until(condition(locator))
#     except TimeoutException:
#         logging.error('error occurred while scraping %s', url, exc_info=True)
#
#
# def scrape_index(page):
#     url = INDEX_URL.format(page=page)
#     scrape_page(url, condition=EC.visibility_of_all_elements_located,
#                 locator=(By.CSS_SELECTOR, '#index .item'))
#
#
# def parse_index():
#     elements = browser.find_elements(By.CSS_SELECTOR, '#index .item .name')
#     for element in elements:
#         href = element.get_attribute('href')
#         yield urljoin(INDEX_URL, href)
#
#
# def scrape_detail(url):
#     scrape_page(url, condition=EC.visibility_of_element_located,
#                 locator=(By.TAG_NAME, 'h2'))
#
#
# def parse_detail():
#     url = browser.current_url
#     name = browser.find_element(By.TAG_NAME, 'h2').text
#     categories = [element.text for element in browser.find_elements(By.CSS_SELECTOR, '.categories button span')]
#     cover = browser.find_element(By.CSS_SELECTOR, '.cover').get_attribute('src')
#     score = browser.find_element(By.CLASS_NAME, 'score').text
#     drama = browser.find_element(By.CSS_SELECTOR, '.drama p').text
#     return {
#         'url': url,
#         'name': name,
#         'categories': categories,
#         'cover': cover,
#         'score': score,
#         'drama': drama
#     }
#
#
# def save_data(data):
#     name = data.get('name')
#     data_path = f'{RESULTS_DIR}/{name}.json'
#     json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
#
#
# def main():
#     try:
#         for page in range(1, TOTAL_PAGE + 1):
#             scrape_index(page)
#             detail_urls = parse_index()
#             for detail_url in list(detail_urls):
#                 logging.info('get detail url %s', detail_url)
#                 scrape_detail(detail_url)
#                 detail_data = parse_detail()
#                 logging.info('detail data %s', detail_data)
#                 save_data(detail_data)
#     finally:
#         browser.close()
#
#
# if __name__ == '__main__':
#     main()