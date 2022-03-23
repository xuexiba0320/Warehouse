import pymysql
from twisted.enterprise import adbapi
from twisted.internet import reactor
reactor.suggestThreadPoolSize(100)

# 异步更新操作
from FangCom.items import IndexItem, DetailItem
import json

class MySQLPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool


    @classmethod
    def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )
        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        """

        if type(item) == type(IndexItem()):
            query = self.dbpool.runInteraction(self.index_insert, item)  # 指定操作方法和操作数据
            # 添加异常处理
            query.addCallback(self.handle_error)  # 处理异常

        if type(item) == type(DetailItem()):
            query = self.dbpool.runInteraction(self.detail_insert, item)  # 指定操作方法和操作数据
            # 添加异常处理
            query.addCallback(self.handle_error)  # 处理异常

    def index_insert(self, cursor, item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        MYSQL_TABLE = 'loupanindex'
        sql = 'REPLACE INTO '+MYSQL_TABLE+'(url, name, unit_price, tag, louaddress, delivery_time, huxin_main,city) VALUES(%s, %s, %s, %s, %s,%s,%s,%s)'
        val = (item['url'],item['name'],item['unit_price'],str(item['tag']),item['louaddress'],
        item['delivery_time'],item['huxin_main'],item['city'])
        # self.u
        cursor.execute(sql, val)
        print('【首页】插入数据库成功！')

    def detail_insert(self, cursor, item):
        MYSQL_TABLE = 'loupanindex'
        url = item['detail_url'].replace('/housedetail', '')
        sql = 'UPDATE '+MYSQL_TABLE+' SET buiding_type=%s,alright=%s,location=%s,property=%s,status=%s,marker_address=%s,phone_plat=%s,floor_area=%s,gross_area=%s,gross_area_ratio=%s,greening_ratio=%s,parking=%s,counter_buidings=%s,counter_households=%s,wuye_corp=%s,wuye_cost=%s,wuye_note=%s,status_buidings=%s WHERE url=%s'

        val = (
        item['buiding_type'],item['alright'],item['location'],
        item['property_'],item['status'],item['marker_address'],item['phone_plat'],
        item['floor_area'],item['gross_area'],item['gross_area_ratio'],item['greening_ratio'],
        item['parking'],item['counter_buidings'],
        item['counter_households'],item['wuye_corp'],item['wuye_cost'],
        item['wuye_note'],item['status_buidings'],url)
        cursor.execute(sql, val)
        print('【详情页】插入数据库成功！')



    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print(failure)






