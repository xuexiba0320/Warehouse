import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from lxml import etree
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue


# selenium模拟登录获取Session + Cookies
class SeleniumLogin(object):
    def __init__(self):
        self.username = 'admin'
        self.password = 'admin'
        self.url = 'https://login2.scrape.center/login'
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        options = webdriver.ChromeOptions()
        options.add_argument('--user-agent={}'.format(ua))
        self.driver = webdriver.Chrome(options=options)

    def open_browser(self):
        self.driver.get(self.url)

    def login(self):
        denglu = (By.XPATH, '//input[@type="text"]')
        WebDriverWait(self.driver, 10, 1).until(EC.visibility_of_element_located(denglu))
        self.driver.find_element(By.XPATH, '//input[@type="text"]').send_keys('admin')
        self.driver.find_element(By.XPATH, '//input[@type="password"]').send_keys('admin')

        # 登录，登录成功后是不是需要切换frame，登录后跳转到：https://login2.scrape.center
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
    
        login_behind = self.driver.current_url

        return login_behind

    def get_message(self):
        cookies = self.driver.get_cookies()
        sessionid = cookies[0]['value']
        cookies = {'sessionid': sessionid}
        # 处理cookie-->dict
        return cookies

    def close_browser(self):
        time.sleep(30)
        self.driver.close()

    def run(self):
        self.open_browser()            # 打开浏览器
        login_behind = self.login()    # 模拟登录
        # 判断是否登录成功
        # -1、URL重定向检查 https://www.cnblogs.com/hiyong/p/15504709.html

        login_finish = 'https://login2.scrape.center/'
        if login_behind in login_finish:
            cookies = self.get_message()      # 获取session、cookies
            # self.close_browser()    # 关闭浏览器
            print('已获得Cookies')
            return cookies


lock = Lock()


def login2():
    # 1、selenium模拟登录获取cookies
    selenium_login = SeleniumLogin()
    cookies = selenium_login.run()

    # 创建队列
    Q = queue.Queue(500)

    # url队列
    with ThreadPoolExecutor(max_workers=1) as executor:
        for num in range(10):
            future = executor.submit(get_initial, cookies, Q, num)

    for i in range(9):
        get_initial(cookies, Q, i)

    """初始页不适用线程（put）,详情页使用线程并且需要加锁才能获取，但是取到一定时间就停止不动了？？？"""

    # 详情页获取
    s = 0
    with ThreadPoolExecutor(max_workers=60) as executor2:
        for j in range(80):
            s += 1
            if s > 10:
                selenium_login = SeleniumLogin()
                cookies = selenium_login.run()
                s = 0
            executor2.submit(get_detail, cookies, Q)
            # 队列出来的时候堵塞，网络慢，无法请求到页面？？？还是产生死锁了？？？


def get_initial(cookies, Q, num):

    # 2、使用登录成功的cookies发起get请求获取响应内容
    url = f'https://login2.scrape.center/page/{num}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers, cookies=cookies).text

    # 获取初始页电影列表
    obj = etree.HTML(response)
    url_list = obj.xpath('//div[@id="index"]//div[@class="el-col el-col-18 el-col-offset-3"]/div')
    data_list = []
    for url in url_list:
        url = url.xpath('.//a[@class="name"]/@href')[0]
        url = 'https://login2.scrape.center' + url
        data_list.append(url)
        # print(url)
        Q.put(url)  # 将url加入队列
        print(Q.qsize(),url)
    print(f'*******************{num+1}/First finish********************')


def get_detail(cookies, Q):
    """

    :param cookies:
    :param Q:
    :return:
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    lock.acquire()
    url = Q.get()


    response = requests.get(url=url, headers=headers, cookies=cookies).text
    # print(response)
    page = etree.HTML(response)
    title = page.xpath('//h2[@class="m-b-sm"]/text()')[0]
    classify = page.xpath('//div[@class="categories"]//span/text()')
    classify = ','.join(classify)
    area = page.xpath('//div[@class="m-v-sm info"]//span/text()')
    # print(area)
    area = [x.strip() for x in area]  # 去除列表中元素的空格和换行
    if '/' in area:
        area.remove('/')   # 如果存在元素‘/’，删除
    area = ','.join(area)         # 将列表连接成字符串
    print(Q.qsize())
    print(title,classify,area)
    Q.task_done()
    lock.release()


if __name__ == '__main__':

    login2()


    # 句柄：新的标签页，如果页面重定向，没有新建标签页，则句柄不变