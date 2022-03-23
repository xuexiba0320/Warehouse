# coding:utf-8
import csv
import datetime
import io
import re
import sys
import time
from urllib import parse as url_parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # 改变标准输出的默认编码

# *******/////2021-12-10:数据对不上，需要重新校核/////******
'''
{   爬取bilibili 指定up主的视频数据
    'name': XXX // 视频名称
    'author': XXX //作者名称
    'date': XXX //发布时间
    'url': XXX //视频链接
    'wachted': XXX //播放量
    'bullet_comments' XXX //弹幕
    'liked': XXX //点赞
    'coin': XXX //投币
    'collected': XXX //收藏
    'shared': XXX //分享
    'now_date': XXX //获取信息时间
}
'''


class BSpider():

    def __init__(self):
        # 某个up主的视频页面，只需对pagenum字段进行替换切换不同的页面
        # 需要安装火狐浏览器与浏览器驱动，将驱动放到python安装根目录下
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.main_url = 'https://space.bilibili.com/upuser_id/video?tid=0&page=page_num&keyword=&order=pubdate'
        self.browser = webdriver.Chrome(options=options)

    def close_webdriver(self):
        self.browser.quit()

    def locate2upuser(self, name_string):
        # 通过名字定位到该up主的ID号
        # 将up主的中文改为url编码
        name_string = url_parse.quote(name_string)
        self.browser.get(
            'https://search.bilibili.com/upuser?keyword=' + name_string + '&from_source=websuggest_search')
        time.sleep(3)

        # 获取当前up的个人链接
        uid = self.browser.find_element(By.XPATH, '//*[@id="user-list"]/div[1]/ul/li/div[2]/div[1]/a[1]').get_attribute(
            'href')
        time.sleep(1)
        # 从链接中取得id
        uid = uid.split('/')[-1].split('?')[0]
        # print(uid)
        return uid

    def resub(self, url, r_pattern, value):
        # 正则替换
        pattern = re.compile(r_pattern)
        page_url = re.sub(pattern, value, url)
        return page_url

    def get_detial_list(self, url):
        # 获取某一页视频 url及名称 列表
        detial_url_list = []
        detial_name_list = []
        self.browser.get(url)
        time.sleep(2)
        html = BeautifulSoup(self.browser.page_source, 'html5lib')
        for a_label in html.find('div', id='submit-video-list').find_all('a',
                                                                         attrs={'target': '_blank', 'class': 'title'}):
            if (a_label['href'] != None):
                detial_url_list.append('https:' + a_label['href'])
                detial_name_list.append(a_label.text)
        return detial_url_list, detial_name_list

    def get_pagenum(self, url):
        # 获取当前up的视频页数
        page_url = url
        page_url = self.resub(page_url, r'page_num', str(1))
        self.browser.get(page_url)
        time.sleep(1)
        html = BeautifulSoup(self.browser.page_source, 'html5lib')

        page_number = html.find('span', attrs={'class': 'be-pager-total'}).text
        return int(page_number.split(' ')[1])

    def get_digit_from_string(self, string):
        # print(string)
        return re.findall(r"\d+\.?\d*", string)[0]

    def get_video_detial(self, video_detial_dect):
        # 获取某个视频的基本信息

        url = video_detial_dect['url']
        self.browser.get(url)
        # 这里的时间设置的大一点，不然页面会加载不出来，
        # 导致获取到的信息为空 可以用浏览器先测试一下多少时间可以获取到这些页面资源
        # 这个由自己电脑的性能和网络决定，出现空值的时候试着将sleep的值调大一点
        time.sleep(5)
        html = BeautifulSoup(self.browser.page_source, 'html5lib')
        # print("视频链接：",url)
        # 清洗数据获取信息，小up主可能部分数据为空 进行正则替换去掉中文 保留数字
        try:
            # 播放量
            video_detial_dect['watched'] = self.get_digit_from_string(
                html.find('span', attrs={'class': 'view'})['title'])
        except Exception as e:
            video_detial_dect['watched'] = ''
        try:
            # 弹幕数
            video_detial_dect['bullet_comments'] = self.get_digit_from_string(
                html.find('span', attrs={'class': 'dm'})['title'])
        except Exception as e:
            video_detial_dect['bullet_comments'] = ''
        try:
            # 点赞
            video_detial_dect['liked'] = self.get_digit_from_string(html.find(
                'span', attrs={'class': 'like'})['title'])
        except Exception as e:
            video_detial_dect['liked'] = ''
        try:
            # 硬币
            video_detial_dect['coin'] = html.find('span', attrs={'class': 'coin'
                                                                 }).get_text().strip()
        except Exception as e:
            video_detial_dect['coin'] = ''
        try:
            # 收藏
            video_detial_dect['collected'] = self.get_digit_from_string(
                html.find('span', attrs={'class': 'collect'})['title'])
        except Exception as e:
            video_detial_dect['collected'] = ''
        try:
            # 转发
            video_detial_dect['shared'] = html.find('span', attrs={'class': 'share'}).get_text().strip().split('\n')[0]
        except Exception as e:
            video_detial_dect['shared'] = ''
            # 发布日期
        try:
            video_detial_dect['date'] = self.browser.find_element(By.XPATH,
                                                                  '//*[@id="viewbox_report"]/div/span[3]').text
        except Exception as e:
            video_detial_dect['date'] = ''
            # 收集时间
            video_detial_dect['now_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            print("清洗数据时发生错误", e)
        # print("视频细节:",video_detial_dect)
        return video_detial_dect

    def get_page(self, upuser_name):
        # 获取一个up 主下的所有视频
        uid = self.locate2upuser(upuser_name)
        url = self.resub(self.main_url, r'upuser_id', str(uid))

        # page_number = 1
        page_number = self.get_pagenum(url)  # 页数
        # 视频url列表 名称列表
        detial_url_list = []
        detial_name_list = []

        for index in range(page_number):
            # print("------------------------------------")
            # print("page: %d" % (index + 1))
            # 对于不同的页，进行正则替换
            page_url = url
            page_url = self.resub(page_url, r'page_num', str(index + 1))
            # print('page_url: %s' % page_url)
            detial_url_list_onepage, detial_name_list_onepage = self.get_detial_list(page_url)
            # 这里要用extend加到后面
            detial_url_list.extend(detial_url_list_onepage)
            # 对视频链接列表进行去重
            url_list = []
            for i in detial_url_list:
                if i not in url_list:
                    url_list.append(i)
            detial_url_list = url_list
            detial_name_list.extend(detial_name_list_onepage)
            # 对视频名称列表进行去重
            name_list = []
            for i in detial_name_list:
                if i not in name_list:
                    name_list.append(i)
            detial_name_list = name_list

        # print("detial_url_list:",detial_url_list)
        # print("detial_name_list:",detial_name_list)

        # 视频json
        video_detial_json = []
        for i in range(len(detial_url_list)):
            video_detial_dect = {}
            video_detial_dect['url'] = detial_url_list[i]
            video_detial_dect['author'] = upuser_name
            video_detial_dect['name'] = detial_name_list[i]
            video_detial_dect = self.get_video_detial(video_detial_dect)
            video_detial_json.append(video_detial_dect)
            print('video_detial_json：', video_detial_json)
            namecsv = detial_name_list[i]
            authorcsv = upuser_name
            datecsv = video_detial_json[0]['date']
            urlcsv = detial_url_list[i]
            wachtedcsv = video_detial_json[0]["watched"]
            bullet_commentscsv = video_detial_json[0]["bullet_comments"]
            likedcsv = video_detial_json[0]["liked"]
            coincsv = video_detial_json[0]["coin"]
            collected = video_detial_json[0]["collected"]
            sharedcsv = video_detial_json[0]["shared"]
            now_datecsv = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open('bilibiliup.csv', 'a', encoding='utf-8', newline='') as csvfile:  # 将数据写到csv文件中
                fieldnames = ['name', 'author', 'date', 'url', 'wachted', 'bullet_comments', 'liked', 'coin',
                              'collected', 'shared', 'now_date']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(
                    {'name': namecsv, 'author': authorcsv, 'date': datecsv, 'url': urlcsv, 'wachted': wachtedcsv,
                     'bullet_comments': bullet_commentscsv, 'liked': likedcsv, 'coin': coincsv,
                     'collected': collected, 'shared': sharedcsv, 'now_date': now_datecsv})


bilibili = BSpider()
print("init done.")
# 更改名字爬取不同的UP视频信息
bilibili.get_page('斑青马')
bilibili.close_webdriver()
