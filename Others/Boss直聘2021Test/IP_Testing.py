# coding:utf-8
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


def ip_test_01(ip_port):
    """使用telnetlib方法检测IP是否可用"""
    ip = ip_port.split(":")[0]
    port = ip_port.split(":")[1]
    try:
        telnetlib.Telnet(ip, port, timeout=3)
        print("代理IP有效！")
    except:
        print("代理IP无效！")


def ip_test_02(ip_port):
    """使用查看网站响应检测IP是否可用，推荐"""
    ip = ip_port.split(':')[0].strip()
    proxy = {'http': ip_port, 'https': ip_port, }
    url = 'http://icanhazip.com'    # IP检测网站
    run = True
    while run:
        try:
            response = requests.get(url=url, proxies=proxy, timeout=10, stream=True)
            print(f'代理使用IP: {ip}, 请求返回IP: {response.text}')
            if response.status_code == 200:
                if response.text.strip() == ip:
                    print(f"{ip_port} IP地址 is Pass!")
                    # IP 返回可用IP地址
                    run = False
                    return ip_port

            else:
                print(f"{ip_port}  IP is Fail!")
                continue
        except requests.exceptions.RequestException as e:
            continue


def main():
    # ip_port = '45.179.164.9:80'
    # 实例化代理IP池调用接口，获取IP
    IpApi()
    parameters = IpApi().get_ip()
    # 再次检测IP可用性（代理IP池已经筛选一次）
    # ip_test_01(ip_port)
    ip_port = ip_test_02(parameters)
    return ip_port


if __name__ == '__main__':
    main()