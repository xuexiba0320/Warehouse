"""使用os，正则提取IP"""
import os, re


def get_realip():
    filename = "ip.swbd"
    # open(filename, "w").write("")
    os.system("ipconfig > {}".format(filename))
    text = open("{}".format(filename)).read()
    # print(text)
    try:
        ipv = re.findall(r'以太网适配器 以太网:(.*?)默认网关', text, re.S)[0]
        ipv4 = re.findall(r'IPv4 地址 . . . . . . . . . . . . :(.*?)子网掩码', ipv, re.S)[0].replace(" ", "")
        ipv6 = re.findall(r'IPv6 地址 . . . . . . . . . . . . :(.*?)临时', ipv, re.S)[0].replace(" ", "")
        print(ipv4)
        print(ipv6)
    except:
        ipv = re.findall(r'以太网适配器 以太网:(.*?)默认网关', text, re.S)[0]
        ipv4 = re.findall(r'IPv4 地址 . . . . . . . . . . . . :(.*?)子网掩码', ipv, re.S)[0].replace(" ", "")
        ipv6 = re.findall(r'IPv6 地址 . . . . . . . . . . . . :(.*?)临时', ipv, re.S)[0].replace(" ", "")
        print(ipv4)
        print(ipv6)
    os.remove(filename)
    return ipv4, ipv6


ip = get_realip()

'''
import socket
myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)
print(myaddr)
会获取虚拟网卡IP地址
'''


"""socket"""
# 下方代码为获取当前主机IPV4 和IPV6的所有IP地址(所有系统均通用)
import socket


def getipaddrs(hostname):
    """Given a host name,perform a standard (forward) lookup and return a list of ip addressfor that host."""
    result = socket.getaddrinfo(hostname, None, 0, socket.SOCK_STREAM)
    return [x[4][0] for x in result]


# calling gethostname() returns the name of the local machine
hostname = socket.gethostname()
print("hostname is:", hostname)

# try to get the fully qualified name:
print("Fully_qualified name:", socket.getfqdn(hostname))
try:
    print("IPv4 address:", getipaddrs(hostname)[-1])
    print("IPv6 address:", getipaddrs(hostname)[3])
except socket.gaierror as e:
    print("error")


"""获取本机外网地址：外网地址每天都在变化吗？？？"""
import requests
response = requests.get("http://txt.go.sohu.com/ip/soip")
ip = re.findall(r'\d+.\d+.\d+.\d+', response.text)
print(ip[0])

rsp = requests.get("http://www.baidu.com", stream=True)
print(rsp.raw._connection.sock.getpeername()[0])
print(rsp.raw._connection.sock.getsockname()[0])