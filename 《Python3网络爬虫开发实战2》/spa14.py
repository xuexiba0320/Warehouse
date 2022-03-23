"""
可以优化：

"""

import requests
# pip install pywasm
import pywasm
import time

# 先下载wasm.wasm文件
wasm = requests.get('https://spa14.scrape.center/js/Wasm.wasm').content
with open('Wasm.wasm', 'wb') as f:
    f.write(wasm)

# 翻页
for i in range(10):

    page = i * 10
    # 获取sign
    t = int(time.time())   # js代码中不是传入字符串吗？.toString()
    vm = pywasm.load('./Wasm.wasm')
    sign = vm.exec('encrypt', [page, t])
    # print(sign)

    url = 'https://spa14.scrape.center/api/movie/'
    data = {
            'limit': '10',
            'offset': page,
            'sign': sign
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    res = requests.get(url=url, headers=headers, params=data)
    print(res.text)
