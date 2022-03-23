import requests
from fake_useragent import UserAgent
import execjs

# 1、实例化一个node对象
node = execjs.get()
# 2、js与文件编译
ctx = node.compile(open('3-签名验证反爬虫（JS逆向）.js', encoding='utf-8').read())
# 3、执行js函数
funcName = 'sign()'
func = ctx.eval(funcName)

params = {
    'actions': func[0],
    'tim': func[1],
    'randstr': func[2],
    'sign': func[3]

}
print(params)

url = 'http://www.porters.vip/verify/sign/fet'
headers = {
    "User-Agent": UserAgent().random,
}

response = requests.get(url=url, headers=headers, params=params).text
print(response)