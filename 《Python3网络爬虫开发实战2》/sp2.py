import requests
import time
import hashlib
import base64


def getHTMLText(url):
    try:
        r=requests.get(url,timeout=60)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.json()
    except:
        pass


for j in range(10):
    #1：时间戳取整
    t=int(time.time())
    #2：SHA1加密
    s1 = f"/api/movie,{t}"
    o = hashlib.sha1(s1.encode("utf-8")).hexdigest()
    s2=f'{o},{t}'
    s3=s2.encode('utf-8')
    #3：Base64加密
    token=base64.b64encode(s3)
    #4:bytes转str
    token=token.decode()

    url=f"https://spa6.scrape.center/api/movie/?limit=10&offset={j*10}&token={token}"
    html=getHTMLText(url)
    for i in range(10):
        print(html['results'][i]['id'],html['results'][i]['name'])
