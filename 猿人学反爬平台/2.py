import requests
import execjs


# 1、实例化一个node对象
node = execjs.get()
# 2、js与文件编译
ctx = node.compile(open('02.js', encoding='utf-8').read())
# 3、执行js函数
funcName = 'get_m_value()'
func = ctx.eval(funcName)
print(func)


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
           'cookie': func
           }


res = requests.get('https://match.yuanrenxue.com/api/match/2', headers=headers).json()
print(res)

