#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Victor"
# Date: 2020/6/18

import socket
import struct
import random

# 内存中的数值为补码表示，所以0xFFFFFFFF是一个负数的补码。
# 负数从补码求原码，最高符号位不变，保持 1， 其余各位求反，末尾加1，也就是 0xFFFFFFFF，
# 二进制为：11111111 11111111 11111111 11111111 
# ->  10000000 00000000 00000000 00000000
# ->  10000000 00000000 00000000 00000001
# 原码首位表示符号位，其余位表示绝对值大小，所以，这个数是 -1


# 1、 struct.pack
# struct.pack用于将Python的值根据格式符，转换为字符串（因为Python中没有字节(Byte)类型，可以把这里的字符串理解为字节流，或字节数组）。
# 其函数原型为：struct.pack(fmt, v1, v2, ...)，参数fmt是格式字符串，关于格式字符串的相关信息在下面有所介绍。
# v1, v2, ...表示要转换的python值。

# 2、 struct.unpack
# struct.unpack做的工作刚好与struct.pack相反，用于将字节流转换成python数据类型。
# 它的函数原型为：struct.unpack(fmt, string)，该函数返回一个元组。

# inet_ntoa， IP地址转换函数， 将ip转换为带点的字符串
# print('{:02X}'.format(i))这个输出是将i以16进制输出，当i是15，输出结果是0F；
# {:X}16进制标准输出形式 02是2位对齐，左补0形式。


def gen_x_forwarded_for_ip(ip_type="ipv4"):
    """
    根据类型返回ip地址
    :param ip_type:
    :return:
    """
    if ip_type == "ipv4":
        ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    elif ip_type == "ipv6":
        ip = ':'.join(['{:x}'.format(random.randint(0, 2 ** 16 - 1)) for i in range(4)]) + ':1'
    else:
        pass

    return ip

if __name__ == '__main__':

    ip = gen_x_forwarded_for_ip("ipv4")
    print(f"IP4: {ip}")

    ip6 = gen_x_forwarded_for_ip("ipv6")
    print(f"IP6: {ip6}")

    # IP4: 76.217.197.148
    # IP6: 289:d8df:b6b7:9086:1