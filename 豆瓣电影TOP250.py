import requests
from fake_useragent import UserAgent
from lxml import etree

# 构建随机请求头
ua = UserAgent().random
headers = {'User-Agent': ua}
print(headers)
# 豆瓣电影TOP250
url = 'https://movie.douban.com/top250'

# 发起requests请求
response = requests.get(url=url, headers=headers).content  # 学习content和text的用法和作用

# ---提取数据---
# 使用xpath提取
obj = etree.HTML(response)
movie_list = obj.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/@href')  # 电影列表

data_list = []
# 遍历每个电影详情页连接发起请求，获取数据
for movie_url in movie_list[0:10]:
    data_dict = {}
    response_movie = requests.get(url=movie_url, headers=headers).content
    obj_detail = etree.HTML(response_movie)
    data_dict['片名'] = obj_detail.xpath('//*[@id="content"]/h1/span[1]/text()')[0]
    data_dict['主演'] = obj_detail.xpath('//*[@id="info"]//span/a[@rel="v:starring"]/text()')[0:5]
    data_dict['类型'] = obj_detail.xpath('///div[@id="info"]//span[@property="v:genre"]/text()')
    data_dict['上映日期'] = obj_detail.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/text()')
    data_dict['片长'] = obj_detail.xpath('//*[@id="info"]/span[@property="v:runtime"]/text()')[0]
    data_list.append(data_dict)

# 写入列表
# movie_name = obj_detail.xpath('//*[@id="content"]/h1/span[1]/text()')[0]
# movie_actor = obj_detail.xpath('//*[@id="info"]//span/a[@rel="v:starring"]/text()')[0:5]
# movie_type = obj_detail.xpath('///div[@id="info"]//span[@property="v:genre"]/text()')
# movie_date = obj_detail.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/text()')
# movie_time = obj_detail.xpath('//*[@id="info"]/span[@property="v:runtime"]/text()')[0]
# list.append(movie_name)
# list.append(movie_actor)
# list.append(movie_type)
# list.append(movie_date)
# list.append(movie_time)

for i in range(len(data_list)):
    print(data_list[i])
    print('*' * 100)
