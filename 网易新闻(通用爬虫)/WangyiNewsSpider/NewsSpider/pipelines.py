# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class NewsspiderPipeline:
    def process_item(self, item, spider):
        print(item['title'], item['time'])
        return item


class MySQLPipeline:
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,         # 数据库端口
            db='News',         # 数据库名
            user='root',       # 数据库用户名
            passwd='1998',     # 数据库密码
            charset='utf8',    # 编码方式
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(
            """insert ignore into nba(title, time, content)
            value (%s, %s, %s)""",      # 纯属python操作mysql知识，不熟悉请恶补
            (item['title'],             # item里面定义的字段和表字段对应
             item['time'],
             item['content'],
             ))

        # 提交sql语句
        self.connect.commit()
        # 必须实现返回
        return item
