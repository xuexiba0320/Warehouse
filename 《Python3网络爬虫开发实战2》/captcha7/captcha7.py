import time
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import ddddocr  # github开源验证码识别库


class Selenium(object):
    def __init__(self):
        """浏览器配置1"""
        # 实例化一个ChromeOptions对象,需导入 from selenium.webdriver import ChromeOptions
        self.options = webdriver.ChromeOptions()
        self.ua = UserAgent().random      # 随机请求头
        self.options.add_argument('--user-agent=' + self.ua)
        self.options.add_argument('--start-maximized')  # 启动时窗口最大化
        self.url = 'https://captcha8.scrape.center'      # url

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

        # 保存截取验证码图片
        self.get_picture()

    def get_picture(self):
        """验证码图片获取"""
        picture = (By.XPATH, '//canvas[@id="captcha"]')
        WebDriverWait(self.driver, 10, 1).until(EC.visibility_of_element_located(picture))
        time.sleep(1)
        # 截取验证图片
        timec = str(time.time()).replace(".", "")
        self.driver.find_element(By.XPATH,'//canvas[@id="captcha"]').screenshot('captcha7_{timec}.png'.format(timec=timec))

    def input_captcha(self):
        # 识别验证图片中的验证码
        ocr = ddddocr.DdddOcr()
        with open("captcha7.png", 'rb') as f:
            image = f.read()

        res = ocr.classification(image)
        print(res)

        captcha = str(res).strip()
        # 输入验证码
        time.sleep(3)
        self.driver.find_element(By.XPATH, '//div[@class="captcha el-input"]/input[@class="el-input__inner"]').send_keys(captcha)
        # 登录
        time.sleep(1)
        login = self.driver.find_element(By.XPATH, '//button[@type="button"]')
        login.click()

    def close_browser(self):
        """关闭浏览器"""
        self.driver.close()
        print('已关闭浏览器')

    def main(self):
        self.set_options()
        # 打开浏览器
        self.open_browser()
        # 模拟登录
        self.login()            # 账号密码
        self.input_captcha()    # 验证码
        # 关闭浏览器
        time.sleep(20)
        self.close_browser()


if __name__ == '__main__':
    Selenium = Selenium()
    Selenium.main()
