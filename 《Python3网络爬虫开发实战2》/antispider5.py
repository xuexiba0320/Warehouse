"""限制单个IP访问频率5分钟最多10次，如果超过则会封禁IP十分钟"""
import requests
from lxml import etree

PROXY_POOL_URL = 'http://localhost:5555/random'


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


proxy = get_proxy()
print(proxy)

num = 1
while True:

    proxies = {
        'http': 'http://' + proxy,
        'https': 'http://' + proxy
    }
    for page in range(1, 11):
        try:

            url = f'https://antispider5.scrape.center/page/{page}'
            response = requests.get(url=url, proxies=proxies)
            # print(response.text)
            obj = etree.HTML(response.text)
            doc = obj.xpath('//div[@class="el-col el-col-18 el-col-offset-3"]/div')
            if not len(doc):
                proxy = get_proxy()
                print('ip have been ban, change a ip:',proxy)
                continue
            else:
                print(len(doc))
                # for i in doc:
                #     title = i.xpath('.//h2[@class="m-b-sm"]/text()')[0]
                #     print(title)

        except Exception:
            proxy = get_proxy()
            print('request have a error, change ip:',proxy)
            continue

