# coding:utf-8
"""
2022-01-02-19:40
"""
import requests
import telnetlib


class IpApi(object):
    """封装代理IP获取接口"""
    @staticmethod
    def get_proxy(self):
        return requests.get("http://127.0.0.1:5010/get").json()

    @staticmethod
    def delete_proxy(proxy):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

    def get_ip(self):
        proxy = self.get_proxy(self).get("proxy")
        self.delete_proxy(proxy)
        return proxy


class IpTest(object):
    def __init__(self):
        self.mark = True

    @staticmethod
    def ip_test_01(ip_port):
        """使用telnetlib方法检测IP是否可用"""
        ip = ip_port.split(":")[0]
        port = ip_port.split(":")[1]
        try:
            telnetlib.Telnet(ip, port, timeout=3)
            print("代理IP有效！")
        except:
            print("代理IP无效！")

    def ip_test_02(self, ip_port):
        """使用查看网站响应检测IP是否可用，推荐"""
        ip = ip_port.split(':')[0].strip()
        proxy = {'http': ip_port, 'https': ip_port, }
        url = 'http://icanhazip.com'    # IP检测网站
        url_baidu = 'http://www.baidu.com'
        try:
            response = requests.get(url=url, proxies=proxy, timeout=10, stream=True)
            print(f'代理使用IP: {ip}, 请求返回IP: {response.text}')
            response_baidu = requests.get(url=url_baidu, proxies=proxy, timeout=10, stream=True)
            if response_baidu.status_code == 200:
                if response.status_code == 200:
                    if response.text.strip() == ip:
                        # print(f"{ip_port} IP地址 is Pass!")
                        # IP 返回可用IP地址
                        self.mark = False
                        return ip_port

        except requests.exceptions.RequestException as e:
            # print(e)
            pass

    def main(self):
        # ip_port = '45.179.164.9:80'
        # 实例化代理IP池调用接口，获取IP
        while self.mark:
            IpApi()
            parameters = IpApi().get_ip()
            # 再次检测IP可用性（代理IP池已经筛选一次）
            # ip_test_01(ip_port)
            ip_port = self.ip_test_02(parameters)
            if ip_port is None:
                continue
            return ip_port


def run():
    # 实例化IP接口类对象
    # ip_api = IpApi()
    # parameters = ip_api.get_ip()

    ip_test = IpTest()
    # 检测方法一
    # ip_test.ip_test_01(parameters)
    # 检测方法二
    ip_port = ip_test.main()
    return ip_port



if __name__ == '__main__':
    """执行程序"""
    run()
