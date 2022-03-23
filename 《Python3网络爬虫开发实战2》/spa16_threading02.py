"""如何实现翻页停止判断"""
import httpx
import pymysql
import time
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed


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

    def create_database(self):
        """创建数据库"""
        pass

    def create_table(self):
        """创建表"""
        pass

    def insert(self, data: tuple):
        """插入"""
        sql = 'INSERT IGNORE INTO spa16(res_id,name,authors,score,cover) values (%s,%s,%s,%s,%s)'
        try:

            self.cursor.execute(sql, data)  # 执行插入语句
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


"""启动数据库服务"""
mysql = MySQL()
"""建立队列对象"""
que = queue.Queue()


def get_data(offset):
    """发起请求"""
    time.sleep(2)
    params = {
            'limit': '18',
            'offset': offset
    }
    url = 'https://spa16.scrape.center/api/book/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    client = httpx.Client(http2=True)
    url_response = client.get(url=url, headers=headers, params=params).json()
    print('第{}页数据【爬取】'.format(int(offset/10+1)))

    """解析数据"""
    res_list = url_response['results']
    data = ''
    data_list = []
    for i in res_list:
        res_id = int(i['id'])
        name = i['name']
        authors = ','.join(i['authors']).replace('\n', '').replace(' ', '')
        score = i['score']
        cover = i['cover']
        data = (res_id, name, authors, score, cover)
        data_list.append(data)
    que.put(data_list)  # 将处理后的数据放入队列


def thread():
    """多线程执行任务"""
    with ThreadPoolExecutor(max_workers=50) as executor:
        future = [executor.submit(get_data, n * 10) for n in range(503)]  # 手动503页？？
        for f in as_completed(future):
            try:
                # 从队列里取出数据存入MySQL
                print("第{}页数据写入MySQL完成！".format((future.index(f)) + 1))
                result = que.get()
                que.task_done()
                for data in result:
                    mysql.insert(data)
            except Exception as e:
                print(e)


def run():
    print('开始抓取数据！！！')
    start_time = time.time()
    # 多线程
    thread()
    # 循环获取结束，断开数据库连接
    mysql.turnoff()
    end_time = time.time()
    print('一共花费了{}秒'.format(end_time-start_time))


if __name__ == '__main__':
    run()
