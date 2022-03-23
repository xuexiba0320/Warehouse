"""
网站：同城二手车
     https://bj.58.com/baoma/?listfrom=dspadvert&PGTID=0d3036e0-0000-1e16-19b4-92f3e56b847f&ClickID=100#mainCon
加密：价格
"""

import requests
import base64
import re
from fontTools.ttLib import TTFont
from lxml import etree
from hashlib import md5
url = 'https://bj.58.com/baoma/?listfrom=dspadvert&PGTID=0d3036e0-0000-1e16-19b4-92f3e56b847f&ClickID=100#mainCon'
headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}
ret = requests.get(url=url,headers=headers)
ret.encoding='utf8'

with open('58.html', 'w', encoding='utf8') as f:
    f.write(ret.text)

with open('58.html', 'r', encoding='utf8') as f:
    ret = f.read()
ba64 = re.findall('base64,(.*?)\'\) forma',ret)[0]
b= base64.b64decode(ba64)
with open('1.woff', 'wb') as f:
    f.write(b)

#
# font_dict = {
#
#     '&#x2d;': 0,
#     '&#x65f6;': 1,
#     '&#x25;': 2,
#     '&#x2f;': 3,
#     '&#x4e07;':4,
#     '&#x2b;':5,
#     '&#xa5;':6,
#     '&#x5143;':7,
#     '&#x8d77;':8,
#     '&#x6298;':9
# }
base_font={'font':[
    {'name':'&#x2d;','value':'3','hex':'f9d6f8bfb0257137ad304bcae1009022'},
    {'name':'&#x65f6;','value':'0','hex':'79a6e23d10c68d14e4ec507e6b02bbf2'},
    {'name':'&#x25;','value':'5','hex':'7125656f5dd35120031671deec325dbe'},
    {'name':'&#x2f;','value':'7','hex':'927faa2e53d85d841839ec58daddb138'},
    {'name':'&#x4e07;','value':'8','hex':'73b0b18ef35ebe5df363bccf4ea5e356'},
    {'name':'&#x2b;','value':'2','hex':'6d6f25ae791948b9b1b6538c4fd5a09b'},
    {'name':'&#xa5;','value':'1','hex':'f3980be01c0bf2e821672497b680f59d'},
    {'name':'&#x5143;','value':'6','hex':'7c26f89c45f85da47fdb94e6edec97b7'},
    {'name':'&#x8d77;','value':'4','hex':'e32ccaa22e9bfc82e927c8c4c5c7487e'},
    {'name':'&#x6298;','value':'9','hex':'415e4dc11caaf995d552a41238fed31d'},
]}
# font = TTFont('1.woff')
# # font.saveXML('1.xml')
# for i in font_dict:
#     print('uni'+i[3:-1].zfill(4).upper())
#     font_cmap = font['glyf'].glyphs.get('uni'+i[3:-1].zfill(4).upper()).data
#     glpyh = md5(font_cmap).hexdigest()
#     print(i,glpyh)
#.getBestCmap()

fot = {

    'uni002D':'&#x2d;',
    'uni65F6':'&#x65f6;',
    'uni0025':'&#x25;',
    'uni002F':'&#x2f;',
    'uni4E07':'&#x4e07;',
    'uni002B':'&#x2b;',
    'uni00A5':'&#xa5;',
    'uni5143':'&#x5143;',
    'uni8D77':'&#x8d77;',
    'uni6298':'&#x6298;',
}
dic = {}
font = TTFont('1.woff')
font.saveXML('1.xml')
font_cmap = font['cmap'].getBestCmap()
uni_list = font_cmap.values()
print(uni_list)
font_n = TTFont('1.woff')
for i in uni_list:
    f = font_n['glyf'].glyphs.get(i).data
    
    glpyh = md5(f).hexdigest()
    for j in base_font.get('font'):
        if j.get('hex')==glpyh:
            dic[fot[i]]=j['value']
print(dic)

with open('58.html', 'r', encoding='utf8') as f:
    ret = f.read()
for i in dic:
    ret = ret.replace(i,dic[i])
page_html = etree.HTML(ret)
lis = page_html.xpath('//*[@id="list"]/ul/li/div')

for li in lis:
    name = ('-').join(li.xpath('../div[1]/a//text()')).replace('\n','').replace('\t','').replace(' ','')
    # money = li.xpath('../div[2]//text()')
    print(name)

