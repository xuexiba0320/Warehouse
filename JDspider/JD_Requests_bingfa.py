import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
from urllib.parse import quote
import grequests


class JDSpider(object):
    def __init__(self, keyword, page_num):
        self.front_url = 'https://search.jd.com/Search?keyword={}&page={}&click=0'.format(keyword, page_num)
        # self.main_url = 'https://search.jd.com/Search?keyword={0}'.format(keyword)
        self.last_url = 'https://search.jd.com/s_new.php?keyword={}&page={}&scrolling=y&log_id=1640257224229.6613&tpl=3_M&isList=0&show_items='.format(keyword, page_num)

        self.front_headers = {
            "user-agent": ua,
            'Host': 'search.jd.com'
        }
        self.last_headers = {
            "user-agent": ua,
            'Referer': self.front_url,
            'Host': 'search.jd.com'
        }

        self.data_list = []  # 存放数据

    def req_web(self):
        """请求网页"""
        front_response = requests.get(url=self.front_url, headers=self.front_headers)
        last_response = requests.get(url=self.last_url, headers=self.last_headers)
        # print(last_response)
        # self.get_data(front_response)
        # self.get_data(last_response)

        req_list = [
            front_response,
            last_response
        ]
        res_list = grequests.map(req_list)  # 并行发送，等最后一个运行完后返回
        print(res_list[0].text)  # 打印第一个请求的响应文本

    # def get_data(self, response):
    #     """解析数据"""
    #     doc = etree.HTML(response)
    #     dataset = doc.xpath('//*[@id="J_goodsList"]/ul/li')
    #     for data in dataset:
    #         data_dict = {}
    #         title = data.xpath('.//div/div[@class="p-name p-name-type-2"]/a/em/text()')
    #         # title添加当前面出现‘京东手机’or‘京东超市’的定位条件
    #         price = data.xpath('.//div/div[@class="p-price"]//i/text()')
    #         shop = data.xpath('.//div/div[@class="p-shop"]//a/@title')
    #         link = data.xpath('.//div/div[@class="p-name p-name-type-2"]/a/@href')[0]
    #
    #         data_dict['标题'] = title
    #         data_dict['价格'] = price
    #         data_dict['店铺'] = shop
    #         data_dict['链接'] = 'https:'+link
    #         self.data_list.append(data_dict)

        # for data in dataset:
        #     title = data.xpath(
        #         './div[@class="gl-i-wrap"]//div[@class="p-name p-name-type-2"]/a/em/text()')[0].strip()
        #     img = 'https:' + str(data.xpath(
        #         './div[@class="gl-i-wrap"]//div[@class="p-img"]/a/img/@data-lazy-img')[0])
        #     price = data.xpath(
        #         './div[@class="gl-i-wrap"]//div[@class="p-price"]/strong/i/text()')
        #     # commit = data.xpath(
        #     #     './div[@class="gl-i-wrap"]//div[@class="p-commit"]/strong/a/text()')
        #     print(title)
        #     # data_Import(title, img, price, keywords)


    def next_page(self):
        pass

    # def save(self):
    #     """保存数据"""
    #     # 将列表字典写入文件
    #     file = 'JD_data.csv'
    #     with open(file, 'w+', encoding='utf-8',newline='') as f:  # 问题： 这里用wb写入会报错
    #         writer = csv.writer(f, dialect='excel')
    #         fieldnames = self.data_list[0].keys()  # solve the problem to automatically write the header
    #         writer.writerow(fieldnames)
    #         for row in self.data_list:
    #             writer.writerow(list(row.values()))

    def main(self):
        """主函数"""
        self.req_web()
        # print(self.data_list)
        # self.save()


if __name__ == '__main__':
    """主程序"""
    ua = UserAgent().random  # 运行程序之前随机获取一个USER-AGENT
    keyword = input('请输入需要查询的商品:')
    page_num = input('请输入需要页数:')
    JDSpider = JDSpider(quote(keyword), page_num)
    JDSpider.main()
