import requests
from fake_useragent import UserAgent
from lxml import etree
import re

url = 'http://www.porters.vip/confusion/flight.html'
headers = {
    "User-Agent": UserAgent().random,
}
response = requests.get(url=url, headers=headers).text
# print(response)

doc = etree.HTML(response)
data = doc.xpath('//div[@class="left col-md-9"]/div[@class="m-airfly-lst"]')
# print(data)


# 找出CSS基准的数据
for i in data:
    # location = i.xpath('.//span[@class="prc_wp"]/@style')
    location = i.xpath('.//em[@class="rel"]/b/@style')
    price = i.xpath('.//em[@class="rel"]/b/i/text()')  # 基准
    print(location,price)
    data = []
# 找出后面数据的位置和值  遍历每一个航班价格
    for j in location:
        # print(j)
        left = re.findall('left:(.*)px', j)[0]
        width = re.findall('width:(.*)px;', j)[0]
        # print(left,width)
        judge = int(int(left)/int(width))  # 排除第一个基准数据

        if judge < -1:
            a = location.index(j)
            # print(a)

            value = i.xpath('.//em[@class="rel"]/b/text()')  # [6,4]
            # print(value)

    #         for k in value:
    #             b = k.replace('\n', '').replace(' ', '').strip()
    #             if b != '':
    #                 value_list.append(b)
    #
    #         for g in value_list:
    #             data.append(g)
    #
    #
    # print(data)


            # print(value)


# 进行CSS偏移覆盖