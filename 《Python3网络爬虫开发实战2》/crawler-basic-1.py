import requests
from lxml import etree


def sum_data():
    url = 'http://www.glidedsky.com/level/web/crawler-basic-1'
    headers = {
        'Cookie':'_ga=GA1.2.319394232.1641218965; _gid=GA1.2.1875179941.1641218965; Hm_lvt_020fbaad6104bcddd1db12d6b78812f6=1641218965; __gads=ID=2bb0ad7f1a64a0c3-2267313da5cf0070:T=1641218965:RT=1641218965:S=ALNI_Mb3tozRGGwJbc_zHBiNiTiq-rtPZA; footprints=eyJpdiI6InlobFNMc2xFbkFPcWFYK0tSVzVJQXc9PSIsInZhbHVlIjoiZndrWGZpMDUrMzdyNTArS0N4cTl5alRGT1c2VFdqY2VISVwvSGFnR1lSYU9PaDJoTnZONE5hZnVlQk01MzZwYUkiLCJtYWMiOiJkNzU1ZTk3YzA1OTRiNGM3ZWNjZGYxOTJiMDdmNzQ1YzFhOTc0NWUyNmI3ODFhZjUzNGE2NDhkODhkMGNiNzgxIn0%3D; XSRF-TOKEN=eyJpdiI6IlZpZ2pBYzV6T3JNUmYxZ3RMQURtUlE9PSIsInZhbHVlIjoib0x3RStHOTgySktkeWlDNTNLYnpVNUNOSFZNa3hZejdRS2ZUbUdoXC9hUW4reUVsdndOV1lrVndVTTZFbFo2b2wiLCJtYWMiOiI0ZTUwYjU0MjhiYTY4ZGRjYTcwZTE5YzQ2NTAyMmVhZjU2ZTI4ZDExZDlhNmI1MzEwNDFlOGM4YzZlMTFmZjZhIn0%3D; glidedsky_session=eyJpdiI6IkNuXC9DMk5obDZ0WDNaMnp5S2h5YU9BPT0iLCJ2YWx1ZSI6ImRYSkdyTjRMMWE3Y1Q4a1dDZXZIS01UdjVIRnJQZVFWSmduK0dkNERqUzBOTUVFaHNCUXIwK2FrTEg0OWYrdG0iLCJtYWMiOiJjNWQ0MjE5NmE0ODAwYmZhZTA4OTVmMmUzZDg0ZGRlZDUxODBmODU0OGYzZWNlYzcwOWNjOWUwMDg2M2I2NGFhIn0%3D; Hm_lpvt_020fbaad6104bcddd1db12d6b78812f6=1641219067',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3880.400 QQBrowser/10.8.4554.400'
    }
    response = requests.get(url=url, headers=headers)
    # print(response.text)
    obj = etree.HTML(response.text)
    data_list = obj.xpath('//*[@class="row"]')
    print(len(data_list))
    num = 0
    for i in data_list:
        data = i.xpath('.//div/text()')
        for j in data:
            num = int(j) + num
    print(num)
        # data.replace('\n', '').replace('\r', '').replace(' ', '')


sum_data()

'''
        # 数据处理   # 正则
        for i in describe:
            a = i.replace('\n', '').replace('\r', '').replace(' ', '')  # 返回的是副本，要赋值给新的变量
            if len(i) > 0:
                self.list.append(a)
                self.list = list(filter(None, self.list))
'''