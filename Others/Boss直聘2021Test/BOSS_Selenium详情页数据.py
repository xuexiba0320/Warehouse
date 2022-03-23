"""
详情页数据请求，cookie几分钟就会失效
2021-12-30 打开显示404提示封ip24小时
"""
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from fake_useragent import UserAgent
from lxml import etree
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import random


class Boss(object):
    def __init__(self):
        """
        --> initialization parameter
        --> Configuring the Browser
        """
        self.ua = UserAgent()
        self.keyword = 'python爬虫'
        self.url = 'https://www.zhipin.com/c100010000/?query={0}&ka=sel-city-100010000'.format(self.keyword)
        """浏览器配置"""
        # 实例化一个ChromeOptions对象,需导入 from selenium.webdriver import ChromeOptions
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=' + self.ua.random)
        # options.add_argument('--log-level=3')
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
            time.sleep(random.randint(1, 6))
            count += 1
            print("正在爬取第{}页数据".format(count))
            try:
                self.parse()
            except Exception as e:
                pass
            else:
                try:
                    # 显性等待出现下一页出现并可以点击 最后下一页无法点击，等待5s后报出异常，try中的except接收异常然后将剩余的几页数据吧保存
                    WebDriverWait(self.driver, 5, 0.5).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[@class="page"]/a[@class="next"]')))
                    self.driver.find_element(By.XPATH, '//div[@class="page"]/a[@class="next"]').click()
                except Exception as e:
                    print('一共{}条数据！！'.format(len(self.data_list)))
                    break
                else:
                    # pass
                    # 测试：设置只爬取一页
                    if count == 1:
                        break

    def parse(self):
        """parse data -> one page"""
        time.sleep(1)
        page = self.driver.page_source   # the type of page_source  -> str
        xp = etree.HTML(page)
        dataset = xp.xpath('//div[@id="main"]//div[@class="job-list"]/ul/li')
        # print(len(dataset))
        for data in dataset:
            link = data.xpath('.//span[@class="job-name"]/a/@href')[0]
            # print(title, area, company, salary, link)
            url = 'https://www.zhipin.com' + link
            self.data_list.append(url)

    def save(self):
        """怎么爬取一定数据就保存起来(不能覆盖之前的)，而不是爬取完才保存？？"""
        return self.data_list

    def requests_url(self):
        """
        使用requests向详情页发起请求需要携带cookie值才能获取数据
        解决cookie失效快：selenium在翻译的时候获取多个cookie（cookie）？然后传给requests发起get请求？？
        2021-12-29：先验证一个cookie可以使用多长时间 or 一个cookie可以发起多少次请求
        """
        print(self.data_list)  # 检测是否拿到岗位url列表
        # headers = {"headers": self.ua.random, "Cookie": 0}
        # url_list = self.save()
        # for url in url_list:
        #     response = requests.get(url=url, headers=headers)
        #     response = response.text

    def main(self):
        """main function"""
        self.open_browser()  # 只能调用一次！！！打开浏览器第一次url就ok
        # time.sleep(2)
        # 点击下一页获取数据
        self.next_page()
        # close browser
        self.driver.close()

        # 详情页requests请求
        self.requests_url()


if __name__ == '__main__':
    Boss = Boss()
    Boss.main()


