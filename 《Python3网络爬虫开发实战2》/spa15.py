import requests
import time
import pywasm


t = len(str(int(time.time()))) << 2  # 位运算
print(t)


# 先下载wasm.wasm文件
wasm = requests.get('https://spa14.scrape.center/js/Wasm.wasm').content
with open('Wasm.wasm', 'wb') as f:
    f.write(wasm)

vm = pywasm.load('./Wasm.wasm')
n = vm.exec('stackAlloc', [t])
print(n)

arg = '/api/movie'


vm = pywasm.load('./Wasm.wasm')
n = vm.exec('encrypt', [t])
print(n)