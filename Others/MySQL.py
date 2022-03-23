"""python连接MySQL
问题:连接数据库时，是要先选用一个数据库（）吗
类中是不是有一个自动调用的函数str、call??
"""
import pymysql


class MySQL(object):
    def __init__(self):       # **arg, **kwarg
        user = {
            'host': '192.168.1.6',  # 服务器IP
            'port': 3306,           # 端口号
            'user': 'root',         # 用户名
            'password': '1998',     # 密码
            'database': 'pytest',   # 数据库名
            'charset': 'utf8'       # 编码格式
        }
        self.database = ''   # 数据库名
        self.TableName = ''  # 表名
        self.row = ''        # 列名
        # self.data = data     # 插入的数据，与列名对应
        self.connect = pymysql.connect(**user)  # 创建连接对象
        self.cursor = self.connect.cursor()     # 获取游标对象
        print('123')

    def create_database(self):
        """创建数据库"""
        pass

    def create_table(self):
        """创建表"""
        pass

    def insert(self):
        """插入"""
        sql = 'INSERT IGNORE INTO spa16(res_id,name,authors,score,cover) values (%s,%s,%s,%s,%s)'
        try:
            self.cursor.execute(sql, self.data)  # 执行插入语句
            self.connect.commit()    # 数据库的存储一类引擎为Innodb，执行完成后需执行commit进行事务提交
        except Exception as e:
            print('数据写入出现异常,执行rollback操作！异常为:', e)
            self.connect.rollback()  # 数据写入出错回滚执行操作

    def modify(self):
        """修改"""
        pass

    def delete(self):
        """删除"""
        pass

    def turnoff(self):
        """关闭"""
        pass

    def __call__(self, *args, **kwargs):
        print('已成功连接到{0}数据库,数据表:{1}。'.format(self.database, self.TableName))


if __name__ == '__main__':
    a = MySQL()
