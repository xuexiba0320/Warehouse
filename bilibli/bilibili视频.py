# coding:utf-8
import os
import re

import requests
from lxml import etree

if __name__ == '__main__':
    url_ = input('请输入网址栏的url:')
    headers_ = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62",
        "Cookie": "i-wanna-go-back=1; _uuid=5123D5FF-FECE-0350-0801-05CD0D97093C35547infoc; buvid3=F785B98D-11FA-4A20-B9E4-4037511DC35C148829infoc; fingerprint=70518f05338e76166c413e2fee8a75ee; buvid_fp=F785B98D-11FA-4A20-B9E4-4037511DC35C148829infoc; buvid_fp_plain=F785B98D-11FA-4A20-B9E4-4037511DC35C148829infoc; SESSDATA=de0c486f%2C1649042689%2Cca28a%2Aa1; bili_jct=e29077ff1a74d454de085dba15fe1cb9; DedeUserID=96924184; DedeUserID__ckMd5=de26ae380e5d6161; sid=j5ldrqkk; blackside_state=1; rpdid=|(u|Jmk)lRmR0J'uYJJRmu|JJ; PVID=1; CURRENT_BLACKGAP=1; video_page_version=v_old_home; CURRENT_QUALITY=80; b_ut=6; CURRENT_FNVAL=2000; b_lsid=496D13EF_17DA2AF3F49; innersign=1",
        "Referer": "https://www.bilibili.com/"
    }
    response_ = requests.get(url_, headers=headers_)
    # 转换类型
    html_body = etree.HTML(response_.text)
    title_namef = html_body.xpath('//title/text()')[0]

    title_name = re.findall(r'(.*?)_哔哩哔哩', title_namef)[0]
    # 提取url
    url_str = html_body.xpath('//script[contains(text(),"window.__playinfo__")]/text()')[0]
    print(url_str)
    video_url = re.findall(r'"video":\[{"id":\d+,"baseUrl":"(.*?)"', url_str)[0]
    print(video_url)
    audio_url = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)"', url_str)[0]
    headers2_ = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62",
        "Cookie": "i-wanna-go-back=1; _uuid=5123D5FF-FECE-0350-0801-05CD0D97093C35547infoc; buvid3=F785B98D-11FA-4A20-B9E4-4037511DC35C148829infoc; fingerprint=70518f05338e76166c413e2fee8a75ee; buvid_fp=F785B98D-11FA-4A20-B9E4-4037511DC35C148829infoc; buvid_fp_plain=F785B98D-11FA-4A20-B9E4-4037511DC35C148829infoc; SESSDATA=de0c486f%2C1649042689%2Cca28a%2Aa1; bili_jct=e29077ff1a74d454de085dba15fe1cb9; DedeUserID=96924184; DedeUserID__ckMd5=de26ae380e5d6161; sid=j5ldrqkk; blackside_state=1; rpdid=|(u|Jmk)lRmR0J'uYJJRmu|JJ; PVID=1; CURRENT_BLACKGAP=1; video_page_version=v_old_home; CURRENT_QUALITY=80; b_ut=6; CURRENT_FNVAL=2000; b_lsid=496D13EF_17DA2AF3F49; innersign=1",
        "Referer": url_
    }
    response_video = requests.get(video_url, headers=headers2_)
    response_audio = requests.get(audio_url, headers=headers2_)

    data_video = response_video.content
    data_audio = response_audio.content

    title_name = re.sub('[\/:*?"<>|]', '', title_name).strip()
    title_new = title_name + "01"
    with open(f"{title_new}.mp4", 'wb+') as f:
        f.write(data_video)
    with open(f"{title_new}.mp3", 'wb') as f:
        f.write(data_audio)
    os.system(f'ffmpeg -i "{title_new}.mp4" -i "{title_new}.mp3" -c copy "{title_name}.mp4"')

    # os.remove(f"{title_new}.mp4")
    # os.remove(f"{title_new}.mp3")
