import requests
import execjs

key_url = 'https://store.steampowered.com/login/getrsakey/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3880.400 QQBrowser/10.8.4554.400'
}
key_data = {
    'donotcache': '1642048835728',
    'username': '1dd9'
}
res = requests.post(url=key_url,data=key_data,headers=headers).json()
print(res)
publickey_mod = res['publickey_mod']
publickey_exp = res['publickey_exp']
print(publickey_mod)
print(publickey_exp)



node = execjs.get()
ctx = node.compile(open('Steam.js',encoding='utf-8').read())
funcName = 'f(123)'
func = ctx.eval(funcName)
print(func)




# url = 'https://store.steampowered.com/login/dologin/'
# data = {
#
#
# }
# response = requests.post(url=url, headers=headers,data=data)
