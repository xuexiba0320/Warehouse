"""
通过设置避开登录滑块，进行模拟滑块登录的时候会出现异常
注意：成功登录后会跳转到个人中心，这时候可能需要将selenium转到个人中心页面再获取成功登录的cookie
一个类怎么调用另一个类里面的初始化参数————？？？继承吗？  类2使用类1中的参数

2021-12-27: 放弃，无法获取cookies。 登录后显示跳转到个人中心显示非法请求，不是进入主页，而是进入个人中心；这次没有验证码出现
            关于selenium+Chrome如何加入全请求头？？？？
"""

import time
from lxml import etree
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import requests


class TaoBaoSelenium(object):
    def __init__(self):
        """初始化参数"""
        self.url = 'https://login.taobao.com/member/login.jhtml?'
        user_agent = UserAgent()
        # self.headers = {'user-agent': user_agent}
        """浏览器配置"""
        options = webdriver.ChromeOptions()
        options.add_argument('--user-agent=' + user_agent.random)
        options.add_argument('--log-level=3')
        options.add_argument("–-referer = https://www.taobao.com/")
        options.add_argument("start-maximized")
        # 忽略证书警告
        options.add_argument('ignore-certificate-errors')
        # 关闭浏览器左上方 ’Chrome正在受到自动测试软件控制‘ 的提示
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(options=options)


        # 更改navigator信息防止被识别出为selenium爬虫
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => false
            })"""})
        # undefined

    def open_browser(self):
        """打开浏览器"""
        self.driver.get(self.url)

    def login(self):
        """ 模拟登录 """
        # 查找账号、密码标签并输入内容
        self.driver.find_element(By.XPATH, '//input[@id="fm-login-id"]').send_keys('18078792825')
        self.driver.find_element(By.XPATH, '//input[@id="fm-login-password"]').send_keys('liningqing1')
        # 淘宝滑块验证处理
        time.sleep(1)
        try:
            slider = self.driver.find_element(By.XPATH, "//span[contains(@class, 'btn_slide')]")
            if slider.is_displayed():
                ActionChains(self.driver).click_and_hold(on_element=slider).perform()
                ActionChains(self.driver).move_by_offset(xoffset=258, yoffset=0).perform()
                ActionChains(self.driver).pause(0.5).release().perform()
        except:
            pass
        finally:
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//button[@class="fm-button fm-submit password-login"]').click()  # 点击
            time.sleep(3)

    def get_cookies(self):
        """获取登录后的cookies值"""
        cookies = self.driver.get_cookies()
        print(cookies)
        return cookies[0]

    def main(self):
        """主函数"""
        self.open_browser()
        self.login()
        self.get_cookies()
        return self.get_cookies()


class TaoBaoRequests(object):
    def __init__(self, cookies, keyword):
        # super().__init__()
        self.url = 'https://s.taobao.com/search?q={}'.format(keyword)
        useragent = UserAgent()
        self.headers = {'user-agent': useragent.random,

                        }
        self.cookies = cookies

    def re_url(self):
        """
        携带cookies发起get请求  +  session会话设置
        https://www.cnblogs.com/dai-zhe/p/14828019.html
        """
        response = requests.get(url=self.url, headers=self.headers).text
        print(self.cookies)
        return response

    def parse(self):
        """'class="row row-2 title"'
        'class="grid g-clearfix"'"""

        response = self.re_url()
        obj = etree.HTML(response)
        data_list = obj.xpath('//div[class="grid g-clearfix"]/div')
        print(len(data_list))
        for data in data_list:
            title = data.xpath('.//div[class="row row-2 title"]/a/text()')
            print(title)


    def main(self):
        self.re_url()
        self.parse()


if __name__ == '__main__':
    """主程序"""
    # 通过selenium登录获取cookies
    TaoBaoSelenium = TaoBaoSelenium()
    cookies = TaoBaoSelenium.main()
    # 使用登录cookies发起requests请求获取数据
    # keyword = input("请输入：")
    # keyword = '手机'
    # TaoBaoRequests = TaoBaoRequests(cookies, keyword)
    # TaoBaoRequests.main()
