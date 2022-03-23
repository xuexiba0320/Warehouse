"""
增加功能：
1、数据处理，去重（url是否重复判断）
2、存入数据库
"""
from selenium import webdriver
from fake_useragent import UserAgent
from lxml import etree
import time
from selenium.webdriver.common.by import By
import csv


class JDSelenium(object):
    def __init__(self, keyword, page_num):
        self.URL = 'https://search.jd.com/Search?keyword={}'.format(keyword)  # 网页不支持中文就进行转码
        self.page_num = page_num
        """Setting Browser Parameters"""
        useragent = UserAgent()
        US = useragent.random
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('user-agent=' + US)
        self.options.add_argument('--log-level=3')
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()  # maximize
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })"""})

    def start_browser(self):
        """start the browser"""
        self.driver.get(self.URL)
        # Simulation page dropdown
        self.dropdown()

    def dropdown(self):
        """Simulation page dropdown"""
        for y in range(15):
            js = 'window.scrollBy(0,500)'
            self.driver.execute_script(js)
            time.sleep(0.1)

    def parse(self):
        """parse data"""
        num = 0
        data_list = []  # 每加载一页就保存到文件中
        while True:
            web_html = self.driver.page_source  # type:str
            doc = etree.HTML(web_html)
            dataset = doc.xpath('//div[@class="gl-i-wrap"]')
            print(len(dataset))
            for data in dataset:
                data_dict = {}
                title = data.xpath('./div[@class="p-name p-name-type-2"]/a/em/text()')
                price = data.xpath('./div[@class="p-price"]//i/text()')
                shop = data.xpath('./div[@class="p-shop"]//a/@title')
                link = data.xpath('./div[@class="p-name p-name-type-2"]/a/@href')[0]
                data_dict['标题'] = title
                data_dict['价格'] = price
                data_dict['店铺'] = shop
                data_dict['链接'] = 'https:' + link
                data_list.append(data_dict)

            num += 1
            print(num)
            if num >= int(self.page_num):
                print('END!!!!')
                break

            # save data
            # self.save(data_list)
            # next page  problem: can click by other way?
            self.driver.find_element(By.XPATH, '//*[@id="J_bottomPage"]/span/a[@class="pn-next"]').click()
            self.dropdown()
            time.sleep(1)

        self.save(data_list)

    @staticmethod
    def save(data_list):
        """save data"""
        print(len(data_list))
        """保存数据"""
        # 将列表字典写入文件
        file = 'JD_data02.csv'
        with open(file, 'w+', encoding='utf-8', newline='') as f:  # 问题： 这里用wb写入会报错
            writer = csv.writer(f, dialect='excel')
            fieldnames = data_list[0].keys()  # solve the problem to automatically write the header
            writer.writerow(fieldnames)
            for row in data_list:
                writer.writerow(list(row.values()))

    def main(self):
        """main function"""
        self.start_browser()
        self.parse()


if __name__ == '__main__':
    """main program"""
    # keyword = input('请输入查询的物品:')
    # page_num = input('请输入查询的页数:')

    keyword = '篮球'
    page_num = '10'

    JDSelenium = JDSelenium(keyword, page_num)
    JDSelenium.main()
