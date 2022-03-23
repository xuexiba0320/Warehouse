import Requests_SecondURL
import Requests_FirstURL
import Selenium_Getcookie


def main():
    # 获取cookie值
    cookie = Selenium_Getcookie.Cookies()
    # 获取初始页url集合
    Requests_FirstURL.BossFirst(cookie)
    # 获取url队列中每个url详情数据
    Requests_SecondURL.BossDetail(cookie)


if __name__ == '__main__':
    main()
