# 1.安装fake_useragent库  pip install fake_useragent
from fake_useragent import UserAgent

# 2、实例化 UserAgent 类
ua = UserAgent()

# 3、随机返回头部信息，推荐使用
print(ua.random)
# 对应浏览器的头部信息
print(ua.ie)
print(ua.opera)
print(ua.chrome)
print(ua.firefox)
print(ua.safari)

# 第一次使用的时候会出现报错，可以通过在实例化UserAgent类的时候添加对应的参数
# 参考：https://blog.csdn.net/yilovexing/article/details/89044980?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_title~default-1.no_search_link&spm=1001.2101.3001.4242.2

r'''socket.timeout: timed out

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "d:\programdata\anaconda3\lib\site-packages\fake_useragent\utils.py", lin
e 166, in load
    verify_ssl=verify_ssl,
  File "d:\programdata\anaconda3\lib\site-packages\fake_useragent\utils.py", lin
e 122, in get_browser_versions
    verify_ssl=verify_ssl,
  File "d:\programdata\anaconda3\lib\site-packages\fake_useragent\utils.py", lin
e 84, in get
    raise FakeUserAgentError('Maximum amount of retries reached')
fake_useragent.errors.FakeUserAgentError: Maximum amount of retries reached'''
