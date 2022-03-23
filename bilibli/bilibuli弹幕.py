# coding:utf-8
import io
import re
import sys

import jieba
# 词云前缀
import matplotlib.pyplot as plt
import pandas as pd
import requests
# 词云生成工具
# 需要对中文进行处理
import wordcloud
from bs4 import BeautifulSoup
from lxml import etree

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码

"""
# 1、获取b站视频url
# 2、得到视频的cid
# 3、通过接口获得弹幕xml文件
# 4、弹幕数据解析
# 5、保存弹幕数据
# 6、弹幕词云
"""


def bilibili():
    # 1、获取b站视频url
    url = 'https://www.bilibili.com/video/BV1Dt411j7bJ'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43'
    }
    # 2、得到视频的cid
    response = requests.get(url=url, headers=headers).text
    doc = etree.HTML(response)
    data = doc.xpath('//script[contains(text(),"window.__playinfo__")]/text()')[0]

    text = doc.xpath('//*[@id="comment"]//p[@class="text"]')
    print(len(text))
    for i in text:
        print(i.xpath('//text()')[0])

    data_1 = re.findall(r'"video":\[{"id":\d+,"baseUrl":"(.*?)"', data)[0]
    cid = re.split('/', data_1)[6]

    # 3、通过接口获得弹幕xml文件, 输入视频对应的cid
    url_data = f'https://comment.bilibili.com/{cid}.xml'
    print(url_data)
    # 4、发起请求
    res_xml = requests.get(url=url_data)

    # 5、弹幕数据解析
    parse = BeautifulSoup(res_xml.content, 'lxml')
    res_1 = parse.find_all('d')

    comments = [comment.text for comment in res_1]  # 因为出来的时候是bs4格式的，我们需要把他转化成list
    print(comments)
    # 6、保存弹幕数据
    return comments

    # 7、弹幕词云


def ciyun(comments):
    comments = [x.upper() for x in comments]  # 统一大小写
    comments_clean = [comment.replace(' ', '') for comment in comments]  # 去掉空格

    set(comments_clean)  # 看一下都有啥类似的没用的词语

    useless_words = ['//TEST',
                     '/TESR',
                     '/TEST',
                     '/TEST/',
                     '/TEXT',
                     '/TEXTSUPREME',
                     '/TSET',
                     '/Y',
                     '\\TEST']

    comments_clean = [element for element in comments_clean if element not in useless_words]  # 去掉不想要的字符
    cipin = pd.DataFrame({'danmu': comments_clean})
    cipin['danmu'].value_counts()  # 查看词频

    danmustr = ''.join(element for element in comments_clean)  # 把所有的弹幕都合并成一个字符串
    words = list(jieba.cut(danmustr))  # 分词
    fnl_words = [word for word in words if len(word) > 1]  # 去掉单字

    wc = wordcloud.WordCloud(width=1000, font_path='simfang.ttf', height=800)  # 设定词云画的大小字体，一定要设定字体，否则中文显示不出来
    wc.generate(' '.join(fnl_words))

    plt.imshow(wc)  # 看图
    wc.to_file("danmu_pic3.png")  # 保存


if __name__ == '__main__':
    """执行程序"""
    data = bilibili()
    ciyun(data)
