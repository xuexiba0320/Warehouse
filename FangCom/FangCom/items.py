import scrapy


class IndexItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    unit_price = scrapy.Field()
    tag = scrapy.Field()
    louaddress = scrapy.Field()
    sale_time = scrapy.Field()
    delivery_time = scrapy.Field()
    huxin_main = scrapy.Field()
    other_name = scrapy.Field()
    part = scrapy.Field()
    compart = scrapy.Field()
    city = scrapy.Field()


class DetailItem(scrapy.Item):
    detail_url = scrapy.Field()
    buiding_type = scrapy.Field()
    alright = scrapy.Field()
    location = scrapy.Field()
    property_ = scrapy.Field()
    status = scrapy.Field()
    marker_address = scrapy.Field()
    phone_plat = scrapy.Field()
    floor_area = scrapy.Field()
    gross_area = scrapy.Field()
    gross_area_ratio = scrapy.Field()
    parking = scrapy.Field()
    counter_buidings = scrapy.Field()
    counter_households = scrapy.Field()
    wuye_corp = scrapy.Field()
    wuye_cost = scrapy.Field()
    wuye_note = scrapy.Field()
    status_buidings = scrapy.Field()
    sale_time = scrapy.Field()
    greening_ratio = scrapy.Field()
