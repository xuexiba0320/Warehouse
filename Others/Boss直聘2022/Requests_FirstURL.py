import requests
from lxml import etree
from fake_useragent import UserAgent
import IP_proxy


class BossFirst(object):
    def __init__(self, cookie):
        # keyword = input('请输入需要查找的岗位:')
        self.ua = UserAgent().random
        self.keyword = 'python爬虫'
        self.city = '100010000'  # 全国城市 代号
        self.position_data = []  # 职位信息列表
        """定时更新请求头-cookie"""
        # 字典推导式参数传入也可
        self.headers = {'Cookie': cookie,
                        'User-Agent': self.ua,
                        'Host': 'www.zhipin.com'
                        }

    # @staticmethod
    # def change_ip():
    #     # 使用代理IP
    #     # ip_port = IP_proxy.run()  # IP获取接口
    #     # proxy = {'http':ip_port, 'https':ip_port}  # 有问题，无法代理到网页中去
    #     proxies = {"http": "http://{}".format(ip_port)}
    #     return proxies

    def request_url(self, url):
        """发起请求"""
        response = requests.get(url=url, headers=self.headers)
        # print(response.url)
        return response.text

    def parse(self, response):
        """数据解析"""
        obj = etree.HTML(response)
        data_list = obj.xpath('//span[@class="job-name"]/a/@href')
        print(len(data_list))
        for data in data_list:
            # 遍历URL集合保存数据到列表中
            data = 'https://www.zhipin.com'+data
            self.position_data.append(data)
            print(data)
        return data_list

    @staticmethod
    def save(data):
        """数据保存"""
        print('保存数据！！')

    def next_page(self):
        """下一页"""
        # 循环前调用一次ip
        # ip_port = self.change_ip()

        page_number = 0
        while True:
            page_number += 1

            url = f'https://www.zhipin.com/c{self.city}/?query={self.keyword}&page={page_number}&ka=page-{page_number}'
            # self.parse(self.request_url(url, ip_port))
            response = self.request_url(url)
            self.parse(response)

            # 翻页结束判断，下一页按钮不可按结束翻页
            if page_number == 2:
                print(f'一共{len(self.position_data)}职位个链接')
                break

    def main(self):
        """主函数"""
        self.next_page()


if __name__ == '__main__':
    cookies = '__zp_stoken__=c818dKQxsOFtlAXUnJWpkBDFGOjoQOlUjPj0XdnFjVXt8WUBMXWA7TDwDaC8gcC9tT11NOhxOXToSfxYNYikgMSxOYC0ZK0MyQ2RjQlQfJmxsOl4LdhdLK3FJUVVQTANxDWR%2FThxEUEctOg0%3D'
    Boss = BossFirst(cookies)
    Boss.main()
#__zp_stoken__=6d98dZxpyJHoxZmFGfnMBCFJ7bHFDZnt6C1lFPX1rdgU3dgNiaUJyDWJUJ2wnORtHAnZ0dExqCkxhNU4fbXcUBSUpbVQpECYTXS0eUEl%2FDXIhETBZKSVBf3NCC1VHbisMQE9GABdsC282dD4%3D