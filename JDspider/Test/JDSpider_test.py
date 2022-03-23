# -*- coding: utf-8 -*-
import os
import re
import time
from urllib.parse import urlencode
import requests
from lxml import etree
import pymysql
from time import strftime, gmtime


# 方法二，从本地文件夹获取


def get_html(keywords, page):
    he = {
             'accept': '*/*',
             'accept-encoding': 'gzip, deflate, br',
             'accept-language': 'zh-CN,zh;q=0.9',
             'cookie': '',
             'referer': '',
             'sec-fetch-mode': 'cors',
             'sec-fetch-site': 'same-origin',
             'x-requested-with': 'XMLHttpRequest',
             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    }

    url = 'https://search.jd.com/Search?keyword=' + keywords + \
          '&qrst=1&stock=1&page=' + str(page) + '&s=51&click=0'
    res = requests.get(url, headers=he, timeout=5)
    res.encoding = 'utf-8'
    source = etree.HTML(res.text)
    data_list = source.xpath('//li[@class="gl-item"]')
    for data in data_list:
        title = data.xpath(
            './div[@class="gl-i-wrap"]//div[@class="p-name p-name-type-2"]/a/em/text()')[0].strip()
        img = 'https:' + str(data.xpath(
            './div[@class="gl-i-wrap"]//div[@class="p-img"]/a/img/@data-lazy-img')[0])
        price = data.xpath(
            './div[@class="gl-i-wrap"]//div[@class="p-price"]/strong/i/text()')
        # commit = data.xpath(
        #     './div[@class="gl-i-wrap"]//div[@class="p-commit"]/strong/a/text()')
        print([title, img, price, keywords])
        # data_Import(title, img, price, keywords)


# 将数据存入mysql中

#
# def data_Import(title, img, price, category):
#     riqi = strftime("%Y-%m-%d %H:%M:%S", gmtime())
#     connection = pymysql.connect(host='192.168.2.176', user='marketing',
#                                  password='anGV5vvyLgNxRom0', db='marketing_api', charset='utf8')
#     try:
#         # 获取会话指针
#         with connection.cursor() as cursor:
#             # 创建SQL语句
#             sql = "INSERT INTO `jd_material`(`id`, `title`, `pic_url`, `price`, `sales`, `create_time`, `category`) VALUES ('',%s,%s,%s,%s,%s,%s);"
#             # 执行SQL语句
#             cursor.execute(sql, (title, img, price, 0, riqi, category))
#             # 提交
#             connection.commit()
#     finally:
#         connection.close()


if __name__ == '__main__':
    # "家用电器", "手机", "运营商", "数码", "电脑", "办公", "家居", "家具", "家装", "厨具", "男装", "女装", "童装", "内衣", "美妆", "个护清洁", "宠物", "女鞋", "箱包", "钟表", "珠宝", "男鞋", "运动", "户外", "房产", "汽车", "汽车用品",
    # "母婴", "玩具乐器", "食品", "酒类", "生鲜", "特产",
    goods_list = ["礼品鲜花"]
    for drnIndex in range(len(goods_list)):
        keywords = goods_list[drnIndex]
        # 定义要爬取的页数
        num = 5
        for page in range(num):
            get_html(keywords, page)
            print('---------------------------')
            time.sleep(2)
            print('第%s页结束' % page)
            time.sleep(2)