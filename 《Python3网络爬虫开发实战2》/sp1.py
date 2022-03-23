"""详情页数据没有爬取sp1\sp2"""

import requests
from lxml import etree
import time
import hashlib
import base64

def sp1():
    for i in range(0,11):
        print(i)
        # 获取token
        time_data = int(time.time())
        print(int(time_data))
        # SHA1
        page_arg = 0
        r = f"/api/movie,{time_data}"
        token_1 = hashlib.sha1(r.encode("utf-8")).hexdigest()

        # Base64
        arg = f"{token_1},{time_data}"
        token_2 = base64.b64encode(arg.encode('utf-8')).decode()

        # r.raise_for_status()
        # return r.json(

        # result = json.loads(r.text)

        # response = r.json()
        #
        # data = response['results']
        # for j in data:
        #     name = j['name']
        #     categories = j['categories']
        #     cover = j['cover']
        #     print(name, categories, cover)

        url = f"https://spa6.scrape.center/api/movie/?limit=10&offset={i * 10}&token={token_2}"
        html = getHTMLText(url)
        for i in range(10):
            print(html['results'][i]['id'], html['results'][i]['name'])



def getHTMLText(url):
    try:
        r=requests.get(url,timeout=60)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.json()
    except:
        pass
if __name__ == '__main__':
    sp1()
