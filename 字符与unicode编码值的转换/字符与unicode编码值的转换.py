str = '27721'
# 获得urlencode编码
str = str.encode('unicode_escape')
# print(str)
# 输出 b'\\u59d3\\u540d'
str=str.decode('utf-8')
# print(str)
# 输出 \u59d3\u540d
str=str.encode('utf-8')
# print(str)
# 输出 b'\\u59d3\\u540d'
str=str.decode('unicode_escape')
# print(str)
# 输出 姓名


from urllib.parse import unquote, quote
kw = '27721'
# 解码
text = unquote(kw, 'utf-8')
print(text)
# 编码
text = quote(text, 'utf-8')
print(text)