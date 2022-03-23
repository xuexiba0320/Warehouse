"""斗鱼直播房间信息爬取202111020
1-获取url
2-创建driver对象
3-发起get请求
4-解析数据
5-保存数据
6-下一页功能
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


# 要是不显示的页面数据是否能够提取？？？
class Douyu(object):
    def __init__(self):
        self.url = 'https://www.douyu.com/directory/all'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def parse_data(self):
        time.sleep(3)
        room_list = self.driver.find_elements(By.XPATH, '//*[@id="listAll"]/section[2]/div[2]/ul/li/div')
        print(len(room_list))  # /a/div[2]/div[1]/h3
        # 遍历每一个房间信息
        all_list = []
        for room in room_list:
            room_dict = {}
            room_dict['title'] = room.find_element(By.XPATH, './a/div[2]/div[1]/h3').text
            room_dict['classification'] = room.find_element(By.XPATH, './a/div[2]/div[1]/span').text
            room_dict['name'] = room.find_element(By.XPATH, './a/div[2]/div[2]/h2/div').text
            #  room_dict['picture'] = room.find_element(By.XPATH, './a/div[1]/div[1]/picture/img').get_attribute('src')
            all_list.append(room_dict)
            print(room_dict)

    def run(self):
        self.driver.get(self.url)
        while True:
            # 自动下划页面
            for y in range(30):
                js = 'window.scrollBy(0,100)'
                self.driver.execute_script(js)
                time.sleep(0.1)
            self.parse_data()
            # next
            try:
                el_next = self.driver.find_element(By.XPATH, '//*[contains(text(),"下一页")]')
                self.driver.execute_script('scrollTo(0,1000000)')
                el_next.click()
            except:
                break


if __name__ == '__main__':
    douyu = Douyu()
    douyu.run()
