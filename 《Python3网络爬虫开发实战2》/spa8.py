import requests
import re
url = 'https://spa8.scrape.center/'
result = requests.get(url).content
# result = result.encode('UTF-8')
result = result.decode('UTF-8')
print(result)
print(type(result))
doc = re.findall(r'const players = [[](.*?)[]];', result, re.S)[0]
print(doc)
doc = re.findall(r'({.*?}),', doc,re.S)
print(doc)
for i in doc:
    name = re.findall('name: "(.*?)"', i)[0]
    image = re.findall('image: "(.*?)"', i)[0]
    birthday = re.findall('birthday: "(.*?)"', i)[0]
    height = re.findall('height: "(.*?)"', i)[0]
    weight = re.findall('weight: "(.*?)"', i)[0]
    print(name,image,birthday,height,weight)
    # 注意：和spa7不同，这里的正则括号相反？？？
