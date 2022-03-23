# coding:utf-8
"""Selenium淘宝模拟登录v1.0:带滑块验证"""

import time
from fake_useragent import UserAgent  # 随机user—agent
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class TaoBao(object):
    def __init__(self):
        # 登录账号
        self.username = 'xxxxx'
        # 登录密码
        self.password = 'xxxxx'

        self.url = 'https://login.taobao.com/'
        # self.url = 'https://www.taobao.com/'
        self.keyword = input('输入你想查找的商品名字:')
        # 修改selenium参数避免被网站识别成selenium爬虫
        # 随机USER-AGENT
        self.USER_AGENT_object = UserAgent()
        self.USER_AGENT = self.USER_AGENT_object.random
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('user-agent=' + self.USER_AGENT)
        self.options.add_argument('--log-level=3')

        # 关闭浏览器左上方 ’Chrome正在受到自动测试软件控制‘ 的提示
        self.options.add_experimental_option('useAutomationExtension', False)
        # 设置为开发者模式，防止被各大网站识别出来使用了Selenium
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()

        # 防检测 -> 更改navigator信息防止被识别出为selenium爬虫：出现滑块，且滑块无法完成验证
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })"""})

    @staticmethod
    def get_track(distance):
        """
        模拟人工滑动轨迹
        :param distance: 移动距离
        :return:
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 1
        # 初速度
        v = 60

        while current < distance:
            if current < mid:
                # 加速度为3
                a = 3
            else:
                # 加速度为-1
                a = -1
            v0 = v
            # 当前速度
            v = v0 + a * t
            # 移动距离
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track  # list 返回的是整个滑动条的多个焦点，可以模拟鼠标的缓慢滑动

    def move_to_gap(self, slider, tracks):
        """
        滑块处理
        :param slider: 滑块
        :param tracks: 移动轨迹
        :return:
        """
        ActionChains(self.driver).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()

    def login(self):
        """
        模拟登录：这里为了节约时间使用了强制元素等待。待优化：使用[显性等待]加载元素再执行操作。
        :return:
        """
        self.driver.get(self.url)
        self.driver.find_element(By.XPATH, '//*[@id="q"]').send_keys(self.keyword)
        self.driver.find_element(By.XPATH, '//*[@id="J_TSearchForm"]/div[1]/button').click()
        time.sleep(2)
        # 查找账号、密码标签并输入内容
        self.driver.find_element(By.XPATH, '//input[@id="fm-login-id"]').send_keys(self.username)
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//input[@id="fm-login-password"]').send_keys(self.password)
        time.sleep(2)

        try:
            if self.driver.find_element(By.XPATH, '//button[@class="fm-button fm-submit password-login"]'):
                print('登录')
                # 点击登录
                self.driver.find_element(By.XPATH, '//button[@class="fm-button fm-submit password-login"]').click()
        except Exception as e:
            print('滑块验证')
            # 找到滑块
            # huakuai = driver.find_element(By.XPATH, '//span[@id="nc_1_n1z"]')
            self.driver.switch_to.frame(
                self.driver.find_element(By.XPATH, '//*[@id="baxia-dialog-content"]'))  # //*[@id="baxia-dialog-content"]
            time.sleep(0.2)
            data = self.driver.find_element(By.XPATH, '//*[@id="nc_1_n1z"]')
            """滑块拉不到最右侧，不松开"""
            self.move_to_gap(data, self.get_track(366))
            time.sleep(0.5)
            # 点击登录
            self.driver.find_element(By.XPATH, '//button[@class="fm-button fm-submit password-login"]').click()

        # 测试：进入商品页面，自动下划页面
        # print(driver.window_handles)
        # driver.switch_to.window(driver.window_handles[0])
        for y in range(85):
            js = 'window.scrollBy(0,100)'
            self.driver.execute_script(js)
            time.sleep(0.1)

    def run(self):
        self.login()


if __name__ == '__main__':
    taobao = TaoBao()
    taobao.run()