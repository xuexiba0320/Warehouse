"""
2021-12-29 可以爬取 ,这个版本没有抓取第一页，因为先点击下一页才进行的数据解析函数parse（）
"""
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from fake_useragent import UserAgent
from lxml import etree
import csv
import time
from selenium.webdriver.common.by import By


class Boss(object):
    def __init__(self):
        """
        --> initialization parameter
        --> Configuring the Browser
        """
        file = 'Boss_selenium.csv'
        self.f = open(file, 'w', encoding='utf-8', newline='')  # w写入，不关闭文件不会覆盖，当关闭文件重新打开会覆盖
        self.writer = csv.writer(self.f, dialect='excel')
        # solve the problem to automatically write the header  -> list
        fieldnames = ['岗位', '地区', '公司', '工资', '链接']
        self.writer.writerow(fieldnames)

        ua = UserAgent().random
        self.keyword = 'python爬虫'
        self.url = 'https://www.zhipin.com/c100010000/?query={0}&ka=sel-city-100010000'.format(self.keyword)
        """浏览器配置"""
        # 实例化一个ChromeOptions对象,需导入 from selenium.webdriver import ChromeOptions
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=' + ua)
        options.add_argument('--log-level=3')
        # 启动时窗口最大化
        options.add_argument('--start-maximized')
        # 关闭浏览器左上方 ’Chrome正在受到自动测试软件控制‘ 的提示
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(options=options)
        # 更改navigator信息防止被识别出为selenium爬虫
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })"""})
        self.data_list = []

    def open_browser(self):
        """open the browser"""
        self.driver.get(self.url)

    def next_page(self):
        """click next page"""
        count = 0
        num = 0
        while True:
            time.sleep(1)
            count += 1
            print("正在爬取第{}页数据".format(count))
            try:
                next_page = self.driver.find_element(By.XPATH, '//div[@class="page"]/a[@class="next"]')
                if next_page.is_displayed():
                    next_page.click()
                else:
                    print("****爬取完成-01****")
                    break
            except Exception as e:
                if count - num < 5:
                    data = self.data_list[30 * num:30 * count]
                    self.save(data)
                    time.sleep(1)
                print('****爬取完成-02****')
                break
            else:
                self.parse()

            # 设置每5页打印一次数据
            if count % 5 == 0:
                num = count
                # 1、分割列表 一段一段保存内容
                data = self.data_list[30 * (count - 5):30 * count]
                self.save(data)
                time.sleep(1)

    def parse(self):
        """parse data -> one page"""
        time.sleep(2)
        page = self.driver.page_source   # the type of page_source  -> str
        xp = etree.HTML(page)
        dataset = xp.xpath('//div[@id="main"]//div[@class="job-list"]/ul/li')
        print(len(dataset))
        for data in dataset:
            data_dict = {}
            title = data.xpath('.//span[@class="job-name"]/a/@title')[0]
            area = data.xpath('.//span[@class="job-area-wrapper"]/span/text()')[0]
            company = data.xpath('.//div[@class="company-text"]/h3/a/text()')[0]
            salary = data.xpath('.//div[@class="job-limit clearfix"]/span/text()')[0]
            link = data.xpath('.//span[@class="job-name"]/a/@href')[0]
            # print(title, area, company, salary, link)

            data_dict = {
                '岗位': title,
                '地区': area,
                '公司': company,
                '工资': salary,
                '链接': 'https://www.zhipin.com' + link
            }
            self.data_list.append(data_dict)

    def save(self, data):
        """怎么爬取一定数据就保存起来(不能覆盖之前的)，而不是爬取完才保存？？"""
        # 将列表字典写入文件
        for row in data:
            self.writer.writerow(list(row.values()))

    def main(self):
        """main function"""
        self.open_browser()  # 只能调用一次！！！打开浏览器第一次url就ok
        time.sleep(2)
        self.next_page()
        # close file
        self.f.close()
        print('一共{}条数据！！'.format(len(self.data_list)))
        print(self.data_list)
        # close browser
        self.driver.close()


if __name__ == '__main__':
    Boss = Boss()
    Boss.main()
