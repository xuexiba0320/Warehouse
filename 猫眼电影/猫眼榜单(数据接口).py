import requests
from fake_useragent import UserAgent
from selenium import webdriver
from lxml import etree
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from urllib.parse import unquote, quote


"""拼图滑块验证码"""

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'uuid_n_v=v1; uuid=21FEC9B0712411EC95431D797208D65730CA46C3AEE14A66A5A7958C970A35B2; _csrf=b7426ce6e24d3c3066a36ea1202678f8fb6e1eb329f3e1b89664419fb4967de1; _lxsdk_cuid=17e3de703aec8-07a09fc8a3b1c1-3354487a-1fa400-17e3de703aec8; _lxsdk=21FEC9B0712411EC95431D797208D65730CA46C3AEE14A66A5A7958C970A35B2; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1641716057,1641733661; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1641733667; __mta=244210362.1641733668173.1641733668173.1641733668173.1; _lxsdk_s=17e3ef39f56-9ff-00e-da0%7C%7C5',
        'Host': 'www.maoyan.com',
        'Referer': 'https://www.maoyan.com/',
        'User-Agent': UserAgent().random
}



def first_url():   # """获取榜单电影"""
    first_url = 'https://www.maoyan.com/board?timeStamp=1641733664374&channelId=40011&index=3&signKey=597cb4aeaa85c9d44a5d31568b72df54&sVersion=1&webdriver=false'   # 可以翻页，但默认定位在广州，选择其他城市后url不变
    response = requests.get(url=first_url, headers=headers)
    print(response.status_code)

    # response = response.text.encode("utf-8").decode()
    # print(response)
    # # obj = etree.HTML(response.text)
    # # url_list = obj.xpath('//dl[@class="movie-list"]//div[@class="movie-item film-channel"]')
    # # url_first_list = []
    # # print(len(url_list))
    # # # for url in url_list:
    # # for url in url_list[0:2]:
    # #     url = 'https://www.maoyan.com' + url.xpath('./a/@href')[0]
    # #     url_first_list.append(url)
    # #     print(url)
    # # return url_first_list


    # 1. 获取binary的内容
    binary_text = response.content
    # 2. 将binary内容转换成字符串,这里使用列binary的方法decode，就是解码
    binary_to_string = binary_text.decode(encoding="utf8")
    print(binary_to_string)

if __name__ == '__main__':
    first_url()
