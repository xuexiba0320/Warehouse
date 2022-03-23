import hashlib
md5 = hashlib.md5()
md5.update("how to use md5 in python hashlib?".encode("utf-8"))  # 注意: 这里面是一个 Unicode-objects
print(md5.hexdigest())
print(type(md5.hexdigest()))  # <class 'str'>
# 输出结果: d26a53750bc40b38b65a520292f69306

# 如果数据量很大，可以分块多次调用update()，最后计算的结果是一样的
md6 = hashlib.md5()
md6.update('how to use md5 in '.encode('utf-8'))
md6.update('python hashlib?'.encode('utf-8'))
print(md6.hexdigest())
# 输出结果: d26a53750bc40b38b65a520292f69306   注意数据要一模一样才会相等，多一个空格都不行


str_md5 = hashlib.md5("how to use md5 in python hashlib?".encode('utf-8')).hexdigest()
print(str_md5)

def get_md5(url):
    """ 包装成一个函数 """
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

print(get_md5("how to use md5 in python hashlib?".encode("utf-8")))
