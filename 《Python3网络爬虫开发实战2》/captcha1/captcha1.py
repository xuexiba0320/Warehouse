import time
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import img_vertical_border as find
from selenium.webdriver import ActionChains
import random


class Selenium(object):
    def __init__(self):
        """浏览器配置1"""
        # 实例化一个ChromeOptions对象,需导入 from selenium.webdriver import ChromeOptions
        self.options = webdriver.ChromeOptions()
        self.ua = UserAgent().random      # 随机请求头
        self.options.add_argument('--user-agent=' + self.ua)
        self.options.add_argument('--start-maximized')  # 启动时窗口最大化
        self.url = 'https://captcha1.scrape.center/'      # url

    def set_options(self):
        """将配置导入Chrome浏览器"""
        self.driver = webdriver.Chrome(options=self.options)

    def open_browser(self):
        """打开浏览器"""
        self.driver.get(self.url)
        time.sleep(1)

    def login(self):
        """控制浏览器"""
        # 一、登录
        denglu = (By.XPATH, '//input[@type="text"]')
        WebDriverWait(self.driver, 10, 1).until(EC.visibility_of_element_located(denglu))
        self.driver.find_element(By.XPATH, '//input[@type="text"]').send_keys('admin')
        self.driver.find_element(By.XPATH, '//input[@type="password"]').send_keys('admin')
        time.sleep(1)
        login = self.driver.find_element(By.XPATH, '//button[@type="button"]')
        login.click()

    def get_picture(self):

        # 这里只能判断验证窗口出来了，但是图片还在加载
        picture = (By.XPATH, '//canvas[@class="geetest_canvas_slice geetest_absolute"]')
        WebDriverWait(self.driver, 10, 1).until(EC.visibility_of_element_located(picture))
        # 这里不知道怎么判断验证码图片是否完全加载，休眠4秒再截图
        time.sleep(3)
        # 截取滑块验证图片
        self.driver.find_element(By.XPATH,'//div[@class="geetest_slicebg geetest_absolute"]').screenshot('captcha1.png')

    @staticmethod
    def get_offset():
        res = find.find_border('captcha1.png', 70)
        print(res)
        offset = abs(res[0]-res[1]) + 39
        print(offset)
        return offset

    @staticmethod
    def get_track(distance):
        """
        拿到移动轨迹，模仿人的滑动行为，先匀加速后均减速
        匀变速运动基本公式：
        ①：v=v0+at
        ②：s=v0t+½at²
        ③：v²-v0²=2as

        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """

        result = []
        current = 0
        mid = distance * 1 / 5
        mid2 = distance * 4 / 5
        t = 0.2
        v = 60
        while current < distance:
            if current < mid:
                a = random.randint(12, 18)
            elif mid <= current < mid2:
                a = random.randint(0, 2)
                v = random.randint(85, 100)
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            s = v0 * t + 0.5 * a * t * t
            current += s
            result.append(round(s))

        s_beyond = distance - current + 2

        result.append(round(s_beyond*1/6))
        result.append(round(s_beyond*3/6))
        result.append(round(s_beyond*2/6))

        result.append(-2)
        result.append(-3)

        result.append(1)
        result.append(2)
        result.append(2)

        return result

        # """分三段"""
        #
        # v = 0         # 初速度
        # t = 0.2       # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        # tracks = []   # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
        # current = 0   # 当前的位移
        #
        # sign1 = distance * 3 / 8  # 加速
        # sign2 = distance * 6 / 8  # 平稳
        #
        # # 第一段
        # while current < distance:
        #     if current < sign1:
        #         a = random.randint(4, 6)         # 加速运动
        #         v0 = v                           # 初速度
        #         s = v0 * t + 0.5 * a * (t ** 2)  # 0.2秒时间内的位移
        #         current += s                     # 当前的位置
        #         tracks.append(round(s))          # 添加到轨迹列表
        #         v = v0 + a * t
        #
        #     elif sign1 < current < sign2:
        #         # 匀速运动
        #         v0 = v
        #         s = v0 * t
        #         tracks.append(round(s))
        #
        #     else:  # sign3 = distance * 6/8 --8/8:
        #         a = -random.randint(2, 3)
        #         v0 = v                           # 初速度
        #         s = v0 * t + 0.5 * a * (t ** 2)  # 0.2秒时间内的位移
        #         current += s                     # 当前的位置
        #         tracks.append(round(s))          # 添加到轨迹列表
        #         v = v0 + a * t
        # print(tracks)
        # return tracks

    def move_slider(self):
        offset = self.get_offset()
        tracks = self.get_track(offset)

        slider = self.driver.find_element(By.XPATH, '//div[@class="geetest_slider_button"]')
        # 按下滑动按键不放
        ActionChains(self.driver).click_and_hold(slider).perform()
        # 向右移动offset距离

        for x in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(random.uniform(0.3, 0.4))
        ActionChains(self.driver).move_by_offset(xoffset=1, yoffset=0).perform()
        time.sleep(random.uniform(0.2, 0.3))
        ActionChains(self.driver).move_by_offset(xoffset=-2, yoffset=0).perform()
        time.sleep(random.uniform(0.1, 0.3))
        ActionChains(self.driver).move_by_offset(xoffset=1, yoffset=0).perform()
        time.sleep(random.uniform(0.8, 1))
        ActionChains(self.driver).release().perform()
        # 松开滑动按键

    def close_browser(self):
        """关闭浏览器"""
        self.driver.close()
        print('已关闭浏览器')

    def main(self):
        self.set_options()
        # 打开浏览器
        self.open_browser()
        # 模拟登录
        self.login()
        # 获取滑块图片
        self.get_picture()
        # 模拟移动滑块
        self.move_slider()
        # 关闭浏览器
        time.sleep(20)
        self.close_browser()


if __name__ == '__main__':
    Selenium = Selenium()
    Selenium.main()
