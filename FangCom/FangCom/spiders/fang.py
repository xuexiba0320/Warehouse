import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from FangCom.items import IndexItem, DetailItem
import re
from bs4 import BeautifulSoup


# 网站域名:fang
host = 'fang'
site = host+'.com'
pageCouner = 0
# 是否只抓取一个城市
isSoloCityOnly = False
# 从相应网站获得 城市的代码 比如郑州是 zz
citycode = 'zz'
start_url = citycode + '.' + site

if isSoloCityOnly:
    startList = ['https://'+start_url]
    ruleList = (
        Rule(LinkExtractor(allow=r'http://'+citycode+'\.'+host+'\.com/$'), callback='dircet_to_family', follow=True),
        )
else:
    startList = ['https://www.'+site+'/SoufunFamily.htm']
    ruleList = (
        Rule(LinkExtractor(allow=r'http://.+\.'+host+'\.com/$'), callback='dircet_to_family', follow=False),
        )


class FangSpider(CrawlSpider):
    name = 'fang'
    allowed_domains = [site]
    start_urls = startList

    # 网页过滤规则
    rules = ruleList

    def parse_item(self, response):
        item = {}
        return item

    def dircet_to_family(self, response):
        """处理城市首页的跳转
        """
        # 提取链接
        newhouse_family = None
        esf_family = None
        zu_family = None
        newhouse_family_list = response.xpath('//a[contains(text(),"新房")]/@href').re('.*new.*')
        if len(newhouse_family_list)>0:
            newhouse_family = newhouse_family_list[0]
        esf_family_list = response.xpath('//a[contains(text(),"二手房")]/@href').re('.*esf.*')
        if len(esf_family_list)>0:
            esf_family = esf_family_list[0]
        zu_family_list = response.xpath('//a[contains(text(),"找租房")]/@href').re('.*zu.*')
        if len(zu_family_list)>0:
            zu_family = zu_family_list[0]

        # 若链接不为空 则将页面交给对应 方法抓取
        if newhouse_family is None:
            pass
        else:
            yield scrapy.Request(newhouse_family, callback=self.parse_family, dont_filter=True)

        # ☑️todo 二手房
        if esf_family is None:
            pass
        else:
            pass

        # ☑️todo 租房信息
        if zu_family is None:
            pass
        else:
            pass
        pass

    def parse_family(self, response):
        """处理新房首页的跳转和抓取
        """
        global pageCouner

        # 获取楼盘信息url列表
        loupans = response.xpath('//div[@id="newhouse_loupan_list"]/ul//li')
        # city = response.xpath('//div[@class="s4Box"]/a/text()').get()
        loupans = loupans.xpath('.//div[@class="nlcd_name"]/a/@href').getall()
        # print('///////',response.url)
        for i in loupans:
            if 'newhouse.fang.com' not in i:
                continue
            else:
                u = response.urljoin(i)
                # print(u)
                yield scrapy.Request(u, callback=self.parse_loupanindex, dont_filter=True)

        # 下一页
        next_page_url = response.xpath('//a[contains(text(),"下一页")]/@href').get()
        if next_page_url is None:
            lis = response.xpath('//li[@class="fr"]/a')
            for index, li in enumerate(lis):
                if index == 0:
                    continue
                if len(li.re('last')) > 0:
                    break
                if len(li.re('active')) > 0:
                    if index + 1 >= len(lis):
                        break
                    url = response.urljoin(lis[index + 1].xpath('./@href').get())
                    print(url)
                    yield scrapy.Request(url, callback=self.parse_family)
                    break
                    # print(UnicodeTranslateError)

        else:
            if True:
                pageCouner += 1
                next_page_url = response.urljoin(next_page_url)
                yield scrapy.Request(next_page_url, callback=self.parse_family)

    def parse_loupanindex(self, response):
        """
        楼盘首页解析
        :param response:
        :return:
        """
        # 名称
        name = response.xpath('//div[@class="tit clearfix"]/h1/strong/text()').get()
        # 标签
        tag_ = response.xpath('//div[@class="biaoqian1"]//text()').getall()
        tag = ''.join(tag_).strip('')
        tag = self.format_text(tag)
        # 价格（每平方）
        unit_price_ = response.xpath('//div[@class="inf_left fl mr10"]//text()').getall()
        unit_price = "".join(unit_price_).strip()
        unit_price = self.format_text(unit_price)
        # 户型
        huxin_main_ = response.xpath('//div[@class="fl zlhx"]//text()').getall()
        huxin_main = "".join(huxin_main_).strip()
        huxin_main = self.format_text(huxin_main)
        # 楼盘地址
        louaddress = response.xpath('//div[@id="xfptxq_B04_12"]/span/text()').get()
        # 开盘时间
        sale_time = ''
        # 交房时间
        deliver_table = response.xpath('//table[@class="tf"]/tbody//tr')
        delivery_time = ''
        for tr in deliver_table:
            delivery_time += "".join(tr.xpath('.//text()').getall()).strip()
        delivery_time = self.format_text(delivery_time)
        # 城市
        city = response.xpath('//div[@class="s4Box"]/a[@href="#"]/text()').get()
        url = response.url
        other_name = ''
        part = ''
        compart = ''
        # print(name)
        # 返回数据到Item
        item = IndexItem(url=response.url, name=name, unit_price=unit_price, tag=tag, louaddress=louaddress,
                                 sale_time=sale_time, delivery_time=delivery_time,
                                 huxin_main=huxin_main, city=city)
        yield item


        # 详情主页中的【楼盘详情】界面url
        # index_url =  'https://zz.newhouse.fang.com/loupan/2510149219.htm'
        # detail_url = 'https://zz.newhouse.fang.com/loupan/2510149219/housedetail.htm'
        detail_url = f"{response.url.rsplit('.', maxsplit=1)[0]}/housedetail.htm"
        yield scrapy.Request(detail_url, callback=self.parse_loupanDetail)


    def parse_loupanDetail(self, response):
        """
        【楼盘详情】页解析
        :param response:
        :return:
        """
        detail_url = response.url
        contents = response.xpath('//div[@class="main-info-price"]/../..').xpath('.//li')[1].get()
        contents = self.format_text(contents)
        bs = BeautifulSoup(contents, 'lxml')
        lis = bs.find_all('li')
        poi_tag = 0
        poi = ''
        buiding_type, alright, location, property_, status,greening_ratio, marker_address, phone_plat, floor_area, gross_area, gross_area_ratio, parking, counter_buidings, counter_households, wuye_corp, wuye_cost, wuye_note, status_buidings, sale_time = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
        for i in lis:
            t = i.get_text().replace(' ', '').replace('\n', '')
            if '建筑类别' in t:
                buiding_type = t.replace('建筑类别：', '')
            elif '装修状况' in t:
                pass
                # 没有考虑
            elif '产权年限' in t:
                alright = t.replace('产权年限：', '')
            elif '环线位置' in t:
                location = t.replace('环线位置：', '')
            elif '开发商' in t:
                property_ = t.replace('开发商：', '')
            elif '销售状态' in t:
                status = t.replace('销售状态：', '')
            elif '开盘时间' in t:
                sale_time = t.replace('开盘时间：', '')
            elif '售楼地址' in t:
                marker_address = t.replace('售楼地址：', '')
            elif '主力户型' in t:
                huxin_main = t.replace('主力户型：', '')
                huxin_main = huxin_main
            elif '预售许可证' in t:
                pass
                # 这里只捕获内容 但不会在这个item中处理
            elif '咨询电话' in t:
                phone_plat = t.replace('咨询电话：', '')
                poi_tag = 1
            elif '占地面积' in t:
                poi_tag = 0
                floor_area = t.replace('占地面积：', '')
            elif poi_tag:
                poi += (t + ' ')
            elif '建筑面积' in t:
                gross_area = t.replace('建筑面积：', '')
            elif '容积率' in t:
                gross_area_ratio = t.replace('容积率：', '')
            elif '绿化率' in t:
                greening_ratio = t.replace('绿化率：', '')
            elif '停车位' in t:
                parking = t.replace('停车位：', '')
            elif '楼栋总数' in t:
                counter_buidings = t.replace('楼栋总数：', '')
            elif '总户数' in t:
                counter_households = t.replace('总户数：', '')
            elif '物业公司' in t:
                wuye_corp = t.replace('物业公司：', '')
            elif '物业费：' in t:
                wuye_cost = t.replace('物业费：', '')
            elif '物业费描述' in t:
                wuye_note = t.replace('物业费描述：', '')
            elif '楼层状况' in t:
                status_buidings = t.replace('楼层状况：', '')
            else:
                pass

        item = DetailItem()
        item['detail_url'] = detail_url
        item['buiding_type'] = buiding_type
        item['alright'] = alright
        item['location'] = location
        item['property_'] = property_
        item['status'] = status
        item['marker_address'] = marker_address
        item['phone_plat'] = phone_plat
        item['floor_area'] = floor_area
        item['greening_ratio'] = greening_ratio
        item['gross_area'] = gross_area
        item['gross_area_ratio'] = gross_area_ratio
        item['parking'] = parking
        item['counter_buidings'] = counter_buidings
        item['counter_households'] = counter_households
        item['wuye_corp'] = wuye_corp
        item['wuye_cost'] = wuye_cost
        item['wuye_note'] = wuye_note
        item['status_buidings'] = status_buidings
        item['sale_time'] = sale_time

        # print(buiding_type)
        yield item



    def format_text(self, text):
        return text.replace('\t', '').replace('\n', '').replace('\xa0', '')

    def format_red(self, text):
        return text.replace('<', '').replace('>', '').replace('"', '').replace(' ', '').replace('/', '')

