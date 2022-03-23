# coding=UTF-8
import random
import re
import time
from time import sleep

import xlrd
import xlwt
from fake_useragent import UserAgent  # 随机user—agent
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from xlutils.copy import copy


# 获取页码
def search_products():
    driver.find_element(By.XPATH, '//*[@id="q"]').send_keys(keyword)
    driver.find_element(By.XPATH, '//*[@id="J_TSearchForm"]/div[1]/button').click()
    time.sleep(3)
    print('*****')
    login()
    print('/////')

    sleep(6)
    token = driver.find_element(By.XPATH, '//*[@id="mainsrp-pager"]/div/div/div/div[1]').text
    # 0代表所有匹配到的数字
    token = int(re.compile('(\d+)').search(token).group(1))
    return token


# 下拉下滑条，加载数据
def drop_down():
    for x in range(1, 11, 2):
        sleep(1)
        j = x / 10
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        driver.execute_script(js)


# 获取商品信息
def get_product(page):
    # oldHandle = driver.window_handles
    # print(oldHandle)
    lis = driver.find_elements(By.XPATH, '//div[@class="items"]/div[@class="item J_MouserOnverReq  "]')
    for i in range(len(lis)):
        print("获取第{}页第{}条中...".format(page, i + 1))
        li = driver.find_elements(By.XPATH, '//div[@class="items"]/div[@class="item J_MouserOnverReq  "]')[i]
        sales = ''
        # 商品信息
        info = li.find_element_by_xpath('.//div[@class="row row-2 title"]').text
        # 价格
        price = li.find_element_by_xpath('.//a[@class="J_ClickStat"]').get_attribute('trace-price')
        # 付款人数
        deal = li.find_element_by_xpath('.//div[@class="deal-cnt"]').text
        # 只留数字,便于数据分析
        deal = int(re.compile('(\d+)').search(deal).group(1))
        # 封面图片地址
        image = li.find_element_by_xpath('.//div[@class="pic"]/a/img').get_attribute('src')
        # 商家名称
        name = li.find_element_by_xpath('.//div[@class="shop"]/a/span[2]').text
        # 商家地址
        site = li.find_element_by_xpath('.//div[@class="location"]').text
        # 详情页地址
        href = li.find_element_by_xpath('.//a[@class="J_ClickStat"]').get_attribute('href')
        li.click()
        handles = driver.window_handles
        # handle = list(set(oldHandle) ^ set(handles))
        # print(handle)
        # oldHandle = list(set(oldHandle) & set(handles))
        driver.switch_to.window(handles)
        # print(driver.switch_to.window(handle[0]))
        storeType = href[8:].split('/')[0]
        if storeType == 'detail.tmall.com':
            # 店铺在天猫上
            driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="baxia-dialog-content"]'))
            driver.find_element(By.XPATH, '//div[@class="baxia-dialog-close"]').click()
            time.sleep(1)
            sales = driver.find_element(By.XPATH, '//*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]').text
        elif storeType == 'item.taobao.com':
            # 店铺在淘宝上
            sales = driver.find_element(By.XPATH, '//*[@id="J_SellCounter"]').text
        else:
            # 既不是天猫也不是淘宝直接跳过
            pass
        # 月销量
        sales = int(re.compile('(\d+)').search(sales).group(1))
        # 月销额
        monthlySales = sales * float(price)
        flag = MakeRandomNumbers(1, 100)
        if flag % 3 == 0 or flag % 8 == 0:
            drop_down()
        # 随机睡眠10~20秒,接口有防盗刷
        markAmount = MakeRandomNumbers(i, len(lis)) % 10
        sleep(MakeRandomNumbers(5 * markAmount, 20 * markAmount))
        driver.close()
        driver.implicitly_wait(10)
        driver.switch_to.window(oldHandle[0])
        value = [[info, price, deal, name, site, sales, monthlySales], ]
        write_excel_xls_append(book_name_xls, value)
        # print(info, price, deal, name, site, sales, monthlySales, image, sep='|')


# 生成随机数
def MakeRandomNumbers(a, b):
    return random.randint(a, b)


# 随机休眠
def dormancy(a, b):
    sleep(random.randint(a, b))


# 翻页
def next_page():
    token = search_products()
    num = 0
    while num != token:
        dormancy(10, 20)  # 随机休眠一到两分钟
        driver.get('https://s.taobao.com/search?q={}&s={}'.format(keyword, 44 * num))
        driver.implicitly_wait(10)
        num += 1
        drop_down()
        get_product(num)


# 创建Excel数据表并写入表头数据
def write_excel_xls_head(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("表头写入成功！")


# 写入表格数据
def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿


def get_track(distance):  # distance为传入的总距离
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
            # 加速度为2
            a = 3
        else:
            # 加速度为-2
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


def move_to_gap(slider, tracks):  # slider是要移动的滑块,tracks是要传入的移动轨迹
    ActionChains(driver).click_and_hold(slider).perform()
    for x in tracks:
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
    time.sleep(0.1)
    ActionChains(driver).release().perform()


def login():
    # 查找账号、密码标签并输入内容
    driver.find_element(By.XPATH, '//input[@id="fm-login-id"]').send_keys('18078792825')
    driver.find_element(By.XPATH, '//input[@id="fm-login-password"]').send_keys('liningqing1')
    # 淘宝滑块验证处理

    try:
        if driver.find_element(By.XPATH, '//button[@class="fm-button fm-submit password-login"]'):
            print('登录')
            driver.find_element(By.XPATH, '//button[@class="fm-button fm-submit password-login"]').click()

    except:
        print('有滑块')
        # 找到滑块
        # huakuai = driver.find_element(By.XPATH, '//span[@id="nc_1_n1z"]')
        driver.switch_to.frame(
            driver.find_element(By.XPATH, '//*[@id="baxia-dialog-content"]'))  # //*[@id="baxia-dialog-content"]
        time.sleep(2)  # 'baxia-dialog-content'
        data = driver.find_element(By.XPATH, '//*[@id="nc_1_n1z"]')
        move_to_gap(data, get_track(400))
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[@class="fm-button fm-submit password-login"]').click()


if __name__ == "__main__":
    book_name_xls = '淘宝商品数据.xls'
    sheet_name_xls = '商品数据表'
    value_title = [["商品信息", "价格", "付款人数", "商家名称", "商家地址", "月销量", "月销金额"], ]
    write_excel_xls_head(book_name_xls, sheet_name_xls, value_title)

    # driver_path = os.path.abspath(os.path.join(os.getcwd(), ".")) + "/dr/chromedriver.exe"
    keyword = input('输入你想查找的商品名字:')

    # options = webdriver.ChromeOptions()
    # # options.add_argument("--no-sandbox")
    # # options.add_argument('lang=zh_CN.UTF-8')
    # options.add_argument('--start-maximized')
    # # options.add_argument("--headless") 无界面模式 options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64;
    # # x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"')
    # # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    # # driver = webdriver.Chrome(executable_path=driver_path, options=options)
    # driver = webdriver.Chrome(options=options)

    USER_AGENT_object = UserAgent()
    USER_AGENT = USER_AGENT_object.random
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=' + USER_AGENT)
    options.add_argument('--log-level=3')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })"""})
    driver.get('https://www.taobao.com/')

    next_page()
