"""
完成
"""
import httpx
import pymysql
import time


def start_mysql():
    """连接数据库，获取数据库控制权限"""
    # 数据库信息
    user = {
        'host': 'localhost',  # 服务器接口
        'port': 3306,  # 端口号
        'user': 'root',  # 用户名
        'password': 'mysql',  # 密码
        'database': 'pytest',  # 数据库名
        'charset': 'utf8'  # 编码格式
    }
    # 创建连接对象
    # conn = pymysql.connect(host=user['host'], port=user['port'], user=user['user'], password=user['password'], database=user['database'], charset=user['charset'])
    connect = pymysql.connect(**user)
    # 获取游标对象
    cursor = connect.cursor()

    # 返回游标进行数据库操作
    return connect, cursor  # -> tuple


connect, cursor = start_mysql()


def request_url(offset):
    """发起请求"""
    params = {
            'limit': '18',
            'offset': offset
    }
    url = 'https://spa16.scrape.center/api/book/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    client = httpx.Client(http2=True)
    res = client.get(url=url, headers=headers, params=params).json()
    print(res)

    return res


def parse(response):
    """解析数据"""
    res_list = response['results']
    data =''
    for i in res_list:
        res_id = int(i['id'])
        name = i['name']
        # 处理 ['\n            悠世', '法老的宠妃']  ['\n            墨舞碧歌']
        authors = ','.join(i['authors']).replace('\n', '').replace(' ', '')
        # authors = i['authors']
        score = i['score']
        cover = i['cover']
        data = (res_id, name, authors, score, cover)
        # print(data)

        # 爬取一页数据就存入一页的数据进mysql
        insert_mysql(data)

    return len(res_list)


def next_page():
    for i in range(503):      # 怎么判断翻页停止，而不是输入503页
        offset = i * 10
        res = request_url(offset)
        judge = parse(res)  # 每存一页就保存一次数据
        print('*'*50)
        print('第{}页数据爬取成功！'.format(i))
        print('*'*50)

        # 循环判断：如果一页的数据小于18条，则到最后一页。最后一页刚刚好为18条数据先不考虑
        if judge < 18:
            break
        # 设置休眠，保证不影响网站运行
        time.sleep(1)


def insert_mysql(data):
    # ’先提前再数据库中创建一个数据表‘
    """
    # create table spa16(
    #     id int unsigned primary key auto_increment not null,
    #     res_id int not null default 000000,
    #     name varchar(200) not null default 'null',
    #     authors varchar(200) not null default 'null',
    #     score varchar(20) not null default 0.0,
    #     cover varchar(200) not null default 'null'
    # );
    """
    # 写入数据
    # 元组连接插入方式  此处的%s为占位符，而不是格式化字符串，所以用%s
    sql_insert = "INSERT IGNORE INTO spa16(res_id,name,authors,score,cover) values (%s,%s,%s,%s,%s)"
    try:
        # 执行插入语句
        cursor.execute(sql_insert, data)
        # 数据库的存储一类引擎为Innodb，执行完成后需执行commit进行事务提交
        connect.commit()
        # cursor.execute('commit')
    except Exception as e:
        # 数据写入出错回滚执行操作
        print('数据写入出现异常,执行rollback操作！异常为:', e)
        connect.rollback()


def close_mysql():
    cursor.close()  # 关闭游标
    connect.close()  # 关闭数据库链接


def run():
    print('开始抓取数据！！！')
    # 循环获取每一页信息
    next_page()
    # 循环获取结束，断开数据库连接
    close_mysql()


if __name__ == '__main__':
    run()
