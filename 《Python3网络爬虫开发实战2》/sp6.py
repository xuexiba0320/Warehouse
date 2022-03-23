"""token有时间限制，js混淆（变量名），没有做翻页的，详情页还没有获取！
base64加密 --->> 前端 ：btoa => base64加密  atob => 解密base64
"""
import requests
import time
import hashlib
import base64

# 生成token
# 时间戳
timestamp = str(int(time.time()))

# /api/movie
# sha1加密
arg1 = ",".join(['/api/movie', timestamp])
arg2 = hashlib.sha1(arg1.encode("utf-8")).hexdigest()
arg3 = ",".join([arg2, timestamp])

# base64加密     前段btoa => base64加密  atob => 解密base64
token = base64.b64encode(arg3.encode('utf-8'))  # 对字符串编码
token = token.decode()
print('token:', token)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}
data = {
        'limit': '10',
        'offset': '10',
        'token': token
}
# url = 'https://spa6.scrape.center/'
url = 'https://spa6.scrape.center/api/movie/'
response = requests.get(url=url, headers=headers, params=data)
print(response.text)
