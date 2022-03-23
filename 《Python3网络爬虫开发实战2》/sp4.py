import requests


def sp3():
    # 实现动态页面下拉刷新数据  问题：如何检测一共有多少页数据，即什么时候停止循环？？
    # num = 1
    for i in range(9):
        num = i*10
        url = 'https://spa4.scrape.center/api/news/?limit=10&offset={}'.format(i*10)
        response = requests.get(url=url).json()
        data = response['results']
        for j in data:
            a = num + data.index(j)
            tilte = j['title']
            url = j['url']
            published_at = j['published_at']
            print(a, tilte, url, published_at)


if __name__ == '__main__':
    sp3()