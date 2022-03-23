import requests
from lxml import etree
from fake_useragent import UserAgent
import IP_proxy


class BossDetail(object):
    def __init__(self, cookie):
        self.ua = UserAgent().random
        self.keyword = 'python爬虫'
        self.url = 'https://www.zhipin.com/job_detail/d547daaef414ce1d1nxy2tS_GFFS.html'
        self.headers = {
            'Cookie': cookie,
            'User-Agent': self.ua,
            'Host': 'www.zhipin.com',
            # 'Referer': 'https://www.zhipin.com/job_detail/?query=python%E7%88%AC%E8%99%AB&city=101280600&industry=&position='
        }
        self.list = []

    @staticmethod
    def change_ip():
        # 使用代理IP
        ip_port = IP_proxy.run()  # IP获取接口
        # proxy = {'http':ip_port, 'https':ip_port}  # 有问题，无法代理到网页中去
        proxies = {"http": "http://{}".format(ip_port)}
        return proxies

    def request_url(self):
        response = requests.get(url=self.url, headers=self.headers)
        print(response.cookies.items())
        return response.text

    def parse(self, response):
        # print(response)
        data = etree.HTML(response)
        describe = data.xpath('//*[@id="main"]//div[@class="detail-content"]/div[@class="job-sec"]/div/text()')
        # 数据处理   # 正则
        for i in describe:
            a = i.replace('\n', '').replace('\r', '').replace(' ', '')  # 返回的是副本，要赋值给新的变量
            if len(i) > 0:
                self.list.append(a)
                self.list = list(filter(None, self.list))

    def save(self):
        print(self.list)

    def main(self):
        self.parse(self.request_url())
        self.save()


if __name__ == '__main__':
    cookies = '__zp_stoken__=e768dJFkUDTl5eXkuFVJJRF1JGkhBMRUuFVoWKlM3E3RNcx1ZeTYLd3xLZm8OUHlHAmRlN2NIYAoRBncVExtJCX4nRzpzblAlYwciWiM4eyIhAwdzKjZTa15uJD0JFCAqQF1XQzg8EAMtXQc%3D'
    Boss = BossDetail(cookies)
    Boss.main()


