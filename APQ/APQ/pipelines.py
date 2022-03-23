# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import codecs
import json


class ApqPipeline:
    # def __init__(self):
    #     self.file = open('data111.json', 'wb')
    #
    # def process_item(self, item, spider):
    #     # 将字典数据序列化
    #     json_data = json.dumps(item)
    #     # 将数据写入文件
    #     self.file.write(json_data)
    #

    # def __init__(self):
    #     # 打开文件,做写入前的准备
    #     self.file = open('1111.json', 'w+', encoding='utf-8')
    #     # 先写入[
    #     self.file.write('[')
    #
    # # 处理item的函数
    # def process_item(self, item, spider):
    #     # 1.把item转换字典类型
    #     item = dict(item)
    #     # 2.把字典对象转换为json字符串
    #     # json.loads() 将json字符串转换python
    #     # json.dumps() 将python对象转换json字符串
    #     json_str = json.dumps(item, ensure_ascii=False)
    #     self.file.write(json_str)
    #     # 写入,逗号 把每个字典分开
    #     self.file.write(',')
    #     # 返回一个item 交给下一个pipeline处理
    #     return item
    #
    # # 爬虫关闭时,将文件填写完整,关闭文件
    # def close_spider(self, spider):
    #     # 将光标移到文件末尾字符之前
    #     # offset偏移量  whence
    #     # 0文件起始位置  1当前位置  2文件末尾
    #     # SEEK_END 文件末尾
    #     # SEEK_SET 文件开始
    #     # SEEK_CUR 当前位置
    #     self.file.seek(-1, os.SEEK_END)
    #     # 删除文件末尾最后一个字符
    #     # truncate() 不填参数,表示从当前的位置截取,当前位置之后的数据都不要
    #     self.file.truncate()
    #     # 写入右括号
    #     self.file.write(']')
    #     # 关闭文件
    #     self.file.close()

    """
    将数据保存到json文件，由于文件编码问题太多，这里用codecs打开，可以避免很多编码异常问题
        在类加载时候自动打开文件，制定名称、打开类型(只读)，编码
        重载process_item，将item写入json文件，由于json.dumps处理的是dict，所以这里要把item转为dict
        为了避免编码问题，这里还要把ensure_ascii设置为false，最后将item返回回去，因为其他类可能要用到
        调用spider_closed信号量，当爬虫关闭时候，关闭文件
    """

    def __init__(self):
        self.file = codecs.open('spiderdata111.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        if len(str(item['date'])) > 4:
            lines = json.dumps(dict(item), ensure_ascii=False) + ',' + "\n"
            self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()
