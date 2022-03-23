import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
from urllib.parse import quote


class JDSpider(object):
    def __init__(self, keyword, page_num):
        self.keyword = keyword
        self.page_num = page_num
        self.front_headers = {
            "user-agent": ua,
            'Host': 'search.jd.com'
        }
        self.data_list = []  # 存放数据

    def req_web(self, front_url, last_url):
        """请求网页"""
        # 模拟后30个数据的请求头：需要用到请求1的url地址就不放在init
        last_headers = {
            "user-agent": ua,
            'Referer': front_url,
            'Host': 'search.jd.com'
        }
        front_response = requests.get(url=front_url, headers=self.front_headers).text
        last_response = requests.get(url=last_url, headers=last_headers).text
        self.get_data(front_response)
        self.get_data(last_response)

    def get_data(self, response):
        """解析数据"""
        # 解析前30个商品信息
        doc = etree.HTML(response)
        dataset = doc.xpath('//div[@class="gl-i-wrap"]')
        print(len(dataset))
        for data in dataset:
            data_dict = {}
            title = data.xpath('./div[@class="p-name p-name-type-2"]/a/em/text()')
            price = data.xpath('./div[@class="p-price"]//i/text()')
            shop = data.xpath('./div[@class="p-shop"]//a/@title')
            link = data.xpath('./div[@class="p-name p-name-type-2"]/a/@href')[0]
            data_dict['标题'] = title
            data_dict['价格'] = price
            data_dict['店铺'] = shop
            data_dict['链接'] = 'https:' + link
            self.data_list.append(data_dict)

    def next_page(self):
        """实现下一页操作"""
        for i in range(0, int(self.page_num)):
            front_url = 'https://search.jd.com/Search?keyword={}&page={}&click=0'.format(self.keyword, 2*(i+1)-1)
            last_url = 'https://search.jd.com/s_new.php?keyword={}&page={}&scrolling=y&log_id=1640257224229.6613&tpl=3_M&isList=0&show_items='.format(
                keyword, 2*(i+1)-1)
            # 前30个商品数据+后30个商品数据
            self.req_web(front_url, last_url)

    def save(self):
        """保存数据"""
        # 将列表字典写入文件
        file = 'JD_data.csv'
        with open(file, 'w', encoding='utf-8', newline='') as f:  # 问题： 这里用wb写入会报错
            writer = csv.writer(f, dialect='excel')
            fieldnames = self.data_list[0].keys()  # solve the problem to automatically write the header
            writer.writerow(fieldnames)
            for row in self.data_list:
                writer.writerow(list(row.values()))

    def main(self):
        """主函数"""
        self.next_page()
        print(self.data_list)
        self.save()


if __name__ == '__main__':
    """主程序"""
    ua = UserAgent().random  # 运行程序之前随机获取一个USER-AGENT
    # keyword = input('请输入需要查询的商品:')
    # page_num = input('请输入需要页数:')
    keyword = '篮球'
    page_num = 10

    JDSpider = JDSpider(quote(keyword), page_num)
    JDSpider.main()

"""
改进:
1  使用多线程
2  requests并发——grequests模块
3  爬取全部页面，自动识别全部页数，自动停止
"""