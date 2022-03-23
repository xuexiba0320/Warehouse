# 案例：asyncio + 不支持异步的模块
import asyncio
import requests


async def download_image(url):
    # 发送网络请求，下载图片（遇到网络下载图片的IO请求，自动化切换到其他任务）
    print('开始下载:', url)

    loop = asyncio.get_event_loop()
    # requests模块默认不支持异步操作，所以需要线程池进行配合
    future = loop.run_in_executor(None, requests.get, url)

    response = await future
    print('下载完成')
    # 保存图片到本地
    file = url.rsplit('_')[-1]
    with open(file, mode='wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    url_list = [
        """
        url1,
        url2,
        url3,
        """
    ]
    tasks = [download_image(url) for url in url_list]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))


# 案例：下载三张图片（网络IO）
# 一、普通方式（同步）
import requests


def download_image(url):
    print('开始下载:', url)
    # 发送网络请求，下载图片
    response = requests.get(url)
    print('图片下载完成')
    # 保存图片到本地
    file = url.rsplit('_')[-1]
    with open(file, mode='wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    url_list = [
        """
        url1,
        url2,
        url3,
        """
    ]

    for item in url_list:
        download_image(item)


# 二、协程方式（异步）
