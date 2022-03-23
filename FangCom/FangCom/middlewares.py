from scrapy import signals
import requests
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import aiohttp


class ProxyMiddleware:
    # def process_request(self, request, spider):
    #     proxy_url = 'http://172.24.247.221:5555/random'
    #     res = requests.get(url=proxy_url)
    #     proxy = res.text
    #     print(f'使用代理:{proxy}')
    #     request.meta['proxy'] = f'http://{proxy}'

    async def process_request(self, request, spider):
        proxy_url = 'http://172.24.247.221:5555/random'
        # 设置超时时间6s
        async with aiohttp.ClientSession() as client:
            res = await client.get(url=proxy_url)
            proxy = await res.text()
            print(f'使用代理:{proxy}')
            request.meta['proxy'] = f'http://{proxy}'
