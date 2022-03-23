# _*_ coding: utf-8 _*_
import gzip
import json
from http.client import HTTPResponse
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup


def get_all_comments_by_bv(bv: str, time_order=False) -> tuple:
    """
    根据哔哩哔哩的BV号，返回对应视频的评论列表（包括评论下面的回复）
    :param bv: 视频的BV号
    :param time_order: 是否需要以时间顺序返回评论，默认按照热度返回
    :return: 包含三个成员的元组，第一个是所有评论的列表（评论的评论按原始的方式组合其中，字典类型）
             第二个是视频的AV号（字符串类型），第三个是统计到的实际评论数（包括评论的评论）
    """
    video_url = 'https://www.bilibili.com/video/' + bv
    headers = {
        'Host': 'www.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': '',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers',
    }
    rep = Request(url=video_url, headers=headers)  # 获取页面
    html_response = urlopen(rep)  # type: HTTPResponse
    html_content = gzip.decompress(html_response.read()).decode(encoding='utf-8')
    bs = BeautifulSoup(markup=html_content, features='html.parser')
    comment_meta = bs.find(name='meta', attrs={'itemprop': 'commentCount'})
    av_meta = bs.find(name='meta', attrs={'property': 'og:url'})

    comment_count = int(comment_meta.attrs['content'])  # 评论总数
    av_number = av_meta.attrs['content'].split('av')[-1][:-1]  # AV号

    print(f'视频 {bv} 的AV号是 {av_number} ，元数据中显示本视频共有 {comment_count} 条评论（包括评论的评论）。')

    page_num = 1
    replies_count = 0
    res = []

    while True:
        # 按时间排序：type=1&sort=0
        # 按热度排序：type=1&sort=2
        comment_url = f'https://api.bilibili.com/x/v2/reply?pn={page_num}&type=1&oid={av_number}' + \
                      f'&sort={0 if time_order else 2}'
        comment_response = urlopen(comment_url)  # type: HTTPResponse
        comments = json.loads(comment_response.read().decode('utf-8'))  # type: dict
        comments = comments.get('data').get('replies')  # type: list
        if comments is None:
            break

        replies_count += len(comments)
        for c in comments:  # type: dict
            if c.get('replies'):
                rp_id = c.get('rpid')
                rp_num = 10
                rp_page = 1
                while True:  # 获取评论下的回复
                    reply_url = f'https://api.bilibili.com/x/v2/reply/reply?' + \
                                f'type=1&pn={rp_page}&oid={av_number}&ps={rp_num}&root={rp_id}'
                    reply_response = urlopen(reply_url)  # type: HTTPResponse
                    reply_reply = json.loads(reply_response.read().decode('utf-8'))  # type: dict
                    reply_reply = reply_reply.get('data').get('replies')  # type: dict

                    if reply_reply is None:
                        break

                    replies_count += len(reply_reply)
                    for r in reply_reply:  # type: dict
                        res.append(r)

                    if len(reply_reply) < rp_num:
                        break
                    rp_page += 1
                c.pop('replies')
                res.append(c)

        if replies_count >= comment_count:
            break
        page_num += 1

    print(f'实际获取视频 {bv} 的评论总共 {replies_count} 条。')
    return res, av_number, replies_count


if __name__ == '__main__':
    cts, av, cnt = get_all_comments_by_bv('BV1ZQ4y1S7e9')
    for i in cts:
        print(i.get('content').get('message'))
