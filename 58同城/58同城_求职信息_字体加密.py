"""58同城字体加密反爬
创建：2021.10.25
维护：2022.03.14 ，58网页结构更新，xpath数据提取更新。58求职简历目前需要添加Cookie值才能获取数据。
"""
import base64
import time
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import numpy
import pytesseract
import requests
from fake_useragent import UserAgent
import re
from lxml import etree
import os


def init():
    """
    初始化请求参数
    :return: url, headers
    """
    # 网址
    url = 'https://gz.58.com/searchjob/?pts=1641557567994'
    # 请求头：58求职简历目前需要添加Cookie值才能获取数据，这里请更换为自己最新的Cookie
    headers = {
        'User-Agent': UserAgent().random,
        'Cookie': 'f=n; id58=CocN02Ie9SCuNKLUEod2Ag==; 58home=gz; f=n; city=gz; commontopbar_ipcity=gz%7C%E5%B9%BF%E5%B7%9E%7C0; 58tj_uuid=efe11e04-cb72-4cd2-b58f-58770f6a44d9; als=0; wmda_uuid=4c3082d3614e6035281138fad861acd8; wmda_new_uuid=1; xxzl_deviceid=AltVC%2FF28ENYx1kpTaMfVmR3Q82NDW67TXSw3Tb31%2FnsYIc%2FrsKLtxRvC8simvlb; sessionid=d3d99c60-2072-4551-8da0-41cbb22a6ef8; fzq_h=748754e47d4074b4beb1d7da482d08f7_1647966816551_b9d3ec499bf44399b77e48de2ccf53b4_1039285430; fzq_js_zhaopin_list_pc=fae313787e4b23a59d9fb6ea5c768c9f_1647966817845_6; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1647966818; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1647966818; param8616=0; param8716kop=1; wmda_visited_projects=%3B11187958619315%3B1731916484865%3B10104579731767; www58com="UserID=64244991225349&UserName=488howc5c"; 58cooper="userid=64244991225349&username=488howc5c"; 58uname=488howc5c; passportAccount="atype=0&bstate=0"; Hm_lvt_a3013634de7e7a5d307653e15a0584cf=1647966862; xxzl_smartid=7fffdd071baadc05e6179462f765c67f; ljrzfc=1; new_uv=2; utm_source=; spm=; init_refer=; wmda_session_id_1731916484865=1647969660948-91c48694-6526-7b63; new_session=0; PPU="UID=64244991225349&UN=488howc5c&TT=9e3b054de41a5f544dce2f4bcbb82dce&PBODY=VBBVtWJ7snANi-t5RpxT1qf8u_hhi3D9noJYiPgrBB2g19qIGiR58V1sQAkyRZH_wYY1hEirxy1kJpr_oVTsc65RcIbT6K7JAzoFGw2IGIkzqbAVfeO-DE1bOBWSRWBSppk9WK-CssNiOSE2QcRUQTkcxl-V_zWRQJzL4oXw--s&VER=1&CUID=i1V7zXUisAHDXLrlKaLMxw"; JSESSIONID=63609AAC4D373F16AD6A136A52CDE581; jl_list_left_banner=5; Hm_lpvt_a3013634de7e7a5d307653e15a0584cf=1647970735; xxzl_cid=de5bb2d467a2484ab052a6aac259c923; xzuid=094d82d6-a7ca-4c2f-b64e-71d1c2f19139'
    }
    return url, headers


def get_html():
    """发起请求"""
    url, headers = init()
    html = requests.get(url=url, headers=headers)
    return html.text


def font_convert(html):
    """
    字体映射关系处理
    :param html: 字体加密的HTML
    :return:
    """
    font_str = re.search('base64,(.*?)\)', html, re.S).group(1)
    # 字体文件解码base64
    debs64 = base64.b64decode(font_str)
    print('字体文件:', debs64)
    # --> b'wOFF\x00\x01\x00\x00\x00\x00.\xc8\x00\ 从解码结果可知是woff文件

    # 保存为woff
    filename = 'font.woff'
    with open(filename, 'wb')as f:
        f.write(debs64)

    # time.sleep(1)
    """这里做个文件判断，文件存在就执行下面操作"""
    if os.path.exists('font.woff'):
        font = TTFont(filename)
        codeList = font.getGlyphOrder()[2:]
        dict_data = font.getBestCmap()   # -->dict
        # 将字典的键值对相互转换
        dict_data = {value: key for key, value in dict_data.items()}
        # 删除第一个无用的数据
        dict_data.pop('x')
        # print(codeList)
        # print(dict_data)

        # # 创建画布
        im = Image.new("RGB", (1800, 1000), (255, 255, 255))
        dr = ImageDraw.Draw(im)

        # # 加载字体文件对象
        font = ImageFont.truetype(filename, 40)
        word_count = len(codeList)
        if word_count >= 40:
            lines = word_count // 40  # 文字排列的行数，在图片上分行展示
        else:
            lines = word_count
        arrayList = numpy.array_split(codeList, lines)

        # 将字体文件中的文字绘制成图片
        for t in range(lines):
            newList = [i.replace("uni", "\\u") for i in arrayList[t]]
            text = "".join(newList)
            text = text.encode('utf-8').decode('unicode_escape')
            dr.text((0, 50 * t), text, font=font, fill="#000000")

        # 可以将图片保存到本地，以便于手动打开图片查看
        im.save("font.jpg")
        im = Image.open("font.jpg")
        result = pytesseract.image_to_string(im, lang="chi_sim")
        # print(result)
        result = result.replace(" ", "").replace("\n", "")
        codeList = [i.replace("uni", "&#x") for i in codeList]
        print(dict(zip(codeList, list(result))))

        return dict(zip(codeList, list(result)))
    else:
        print('没有成功下载字体文件，请重新执行！')


def parse(html, font_map):
    """
    :param html: 字体加密的HTML网页
    :param font_map: 字体映射关系
    :return:
    """
    # 根据字体映射关系进行文字替换
    new_html = html
    for key, value in font_map.items():
        # print(key.lower())
        new_html = re.sub(key.lower()+';', value, new_html)

    # 对替换后的HTML网页数据进行xpath解析、提取
    obj = etree.HTML(new_html)
    data_list = obj.xpath('//div[@id="infolist"]/ul/li//dd[@class="fl overflowauto"]')  # 35个简历信息
    for data in data_list:
        dict_data = {}
        dict_data = {
                     '【性别】': data.xpath('.//div[@class="infocardMessageOne"]//div[@class="clearfix"]/em[1]/text()')[0],
                     '【年龄】': data.xpath('.//div[@class="infocardMessageOne"]//div[@class="clearfix"]/em[2]/text()')[0],
                     '【工作时间】': data.xpath('.//div[@class="infocardMessageOne"]//div[@class="clearfix"]/em[3]/text()'),
                     '【学历】': data.xpath('.//div[@class="infocardMessageOne"]//div[@class="clearfix"]/em[4]/text()')[0],
                     '【期望职业】': data.xpath('.//p[1]/span/text()')[0],
                     '【现职业】': data.xpath('.//p[1]/em[2]/text()'),
                     '【期望地点】': data.xpath('.//p[@class="placeDesire"]/span/text()')[0],
                     }
        print(dict_data)


def run():
    # 获取替换前的HTML
    html = get_html()
    # 获取字体文件
    font_map = font_convert(html)
    # 解析
    parse(html, font_map)


if __name__ == '__main__':
    run()