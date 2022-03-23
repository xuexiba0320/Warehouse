"""区分输入的IP地址是IPv4 还是 IPv6"""
import IPy


ip_address = "192.168.1.3"

ip_type = IPy.IP(ip_address).version()
print(ip_type)

ip_type = IPy.IP(ip_address).strHex()
print(ip_type)

ip_type = IPy.IP(ip_type)
print(ip_type)