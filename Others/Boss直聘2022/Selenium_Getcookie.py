import time
from selenium import webdriver
from fake_useragent import UserAgent
import IP_proxy


class Cookies(object):
    def __init__(self):
        """浏览器配置1"""
        self.options = webdriver.ChromeOptions()
        self.ua = UserAgent().random
        self.options.add_argument('--user-agent=' + self.ua)
        # 设置日志提示等级
        # options.add_argument('--log-level=3')
        # 关闭浏览器左上方 ’Chrome正在受到自动测试软件控制‘ 的提示
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])

        self.url = 'https://www.zhipin.com/job_detail/?query=python%E7%88%AC%E8%99%AB&city=100010000&industry=&position='

    def set_options(self):
        """配浏览器配置2"""
        # 代理IP
        mark = False
        if mark:
            ip_port = IP_proxy.run()
            self.options.add_argument('--proxy-server=http://{0}'.format(ip_port))
        self.driver = webdriver.Chrome(options=self.options)

    def open_browser(self):
        """打开浏览器"""
        self.set_options()
        self.driver.get(self.url)

    def get_cookie(self):
        """获取打开网页的cookie值"""
        cookies = self.driver.get_cookies()  # -> list
        # cookie 处理 --> 取出__token_的对应的值
        for cookie in cookies:
            if cookie['name'] == '__zp_stoken__':
                print('最新cookie值为:', cookie['value'])
                return cookie['value']   # 退出函数

    def close_browser(self):
        """关闭浏览器"""
        self.driver.quit()

    def main(self):
        self.open_browser()
        # 如何判断是否拿到cookie
        self.get_cookie()
        # self.close_browser()


if __name__ == '__main__':
    Selenium = Cookies()
    Selenium.main()
