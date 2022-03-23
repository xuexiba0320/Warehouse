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

file = '1.js'
# 创建node对象
node = execjs.get()
# 编译js文件
ctx = node.compile(open(file).read())

# 执行Js
js = f"getToken({json.dumps(item, ensure_ascii=False)})"
print(js)
func = ctx.eval(js)
print(func)