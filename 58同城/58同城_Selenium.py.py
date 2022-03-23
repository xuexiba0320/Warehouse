from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from urllib.parse import unquote, quote


class Selenium(object):
    def __init__(self):
        """浏览器配置1"""
        # 实例化一个ChromeOptions对象,需导入 from selenium.webdriver import ChromeOptions
        self.options = webdriver.ChromeOptions()
        # 随机请求头
        self.ua = UserAgent().random
        self.options.add_argument('--user-agent=' + self.ua)

        # 设置日志提示等级
        self.options.add_argument('--log-level=3')

        # 启动时窗口最大化
        # self.options.add_argument('--start-maximized')

        # 关闭浏览器左上方 ’Chrome正在受到自动测试软件控制‘ 的提示
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # url
        # self.url = 'https://passport.58.com/login?path=https%3A%2F%2Fmy.58.com%2Findex'
        self.url = 'https://passport.58.com/login/?path=https://gz.58.com/searchjob/%3Fpts%3D1641557296383'
        data = unquote(self.url, 'utf-8')
        print(data)

    def set_options(self):
        """
        配浏览器配置2
            --启动代理IP（默认关闭）
            --更改navigator信息
        """
        # ip_agent = False
        # if ip_agent:
        #     ip_port = IP_Testing.run()
        #     self.options.add_argument('--proxy-server=http://{0}'.format(ip_port))
        #     print(ip_port)
        #     print(self.ua)

        # 将配置导入Chrome浏览器
        self.driver = webdriver.Chrome(options=self.options)
        # 更改navigator信息防止被识别出为selenium爬虫
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })"""})

    def open_browser(self):
        """打开浏览器"""
        # self.driver.get('http://icanhazip.com')
        self.driver.get(self.url)

    def control_browser(self):
        """控制浏览器"""

        locator = (By.ID, 'mask_body_item_newpassword')
        WebDriverWait(self.driver, 10, 1).until(EC.presence_of_element_located(locator))

        time.sleep(random.randint(1, 2))
        self.driver.find_element(By.ID, 'mask_body_item_username').send_keys('18078792825')
        time.sleep(random.randint(1, 3))
        self.driver.find_element(By.ID, 'mask_body_item_newpassword').send_keys('xuexiba1998.')

        login = (By.ID, 'mask_body_item_login')
        WebDriverWait(self.driver, 5, 1).until(EC.element_to_be_clickable(login))
        time.sleep(random.randint(1, 2))
        self.driver.find_element(By.ID, 'mask_body_item_login').click()

    def parse(self):

        #
        time.sleep(1)
        search_window = self.driver.current_window_handle

        aa = self.driver.page_source
        print(aa)

    def close_browser(self):
        """关闭浏览器"""
        self.driver.quit()
        # self.driver.close()

    def main(self):
        self.set_options()
        # time.sleep(10)
        self.open_browser()
        self.control_browser()
        self.parse()
        time.sleep(30)
        self.close_browser()


if __name__ == '__main__':
    Selenium = Selenium()
    Selenium.main()
