# import requests
# from lxml import etree  # xpath 能处理非结构化的数据吗？？
# import re  # 正则匹配中括号 (.*)\[([^\[\]]*)\](.*)   [[](.*?)[]]
# import json
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
# }
# url = 'https://spa7.scrape.center/js/main.js'
# response = requests.get(url=url, headers=headers)
# doc = re.findall(r'const players = [[](.*?)[]]', response.text, re.S)[0]
# doc = re.findall(r'({.*?}),', doc,re.S)
# for i in doc:
#     name = re.findall("name: '(.*?)'", i)[0]
#     image = re.findall("image: '(.*?)'", i)[0]
#     birthday = re.findall("birthday: '(.*?)'", i)[0]
#     height = re.findall("height: '(.*?)'", i)[0]
#     weight = re.findall("weight: '(.*?)'", i)[0]
#     print(name,image,birthday,height,weight)


import execjs
import requests
import json

item = {
    'name': '克里斯-保罗',
    'image': 'paul.png',
    'birthday': '1985-05-06',
    'height': '185cm',
    'weight': '79.4KG'
}

file = 'sp7.js'
# 创建node对象
node = execjs.get()
# 编译js文件
ctx = node.compile(open(file).read())

# 执行Js
js = f"getToken({json.dumps(item, ensure_ascii=False)})"
print(js)
func = ctx.eval(js)
print(func)