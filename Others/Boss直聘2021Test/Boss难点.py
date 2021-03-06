"""
爬取Boss直聘主要有以下难点：
        在不登陆的情况下最多爬十页就会出现手动打码验证
        出现大概五六次手动打码后就会封禁ip地址，封禁1天的时间
解决办法
    1、切换ip
    这里我尝试过很多收费代理，免费代理，几乎都骗不过去，建议不要用。
    可以采用连接手机wifi的方式，手机开热点，当封禁ip时将手机调成飞行模式，再关掉。这时会给你重新分配一个ip地址，就可以继续了。
2、登录
    当你爬取的数据很多时，不可能一直看着开飞行模式，太浪费时间，因此可以采取登录的方式。
    登录获取cookies
    在网页登录账号，拿到cookies进行爬取，就可以爬取大量数据，但也存在问题，cookies失效快，需要重新获取。
    模拟浏览器
    采用模拟浏览器的方式，并且采用本地浏览器方式，可以selenium模拟浏览器爬取（淘宝、微博等需要登陆验证的网站）多次登陆问题，这样做的好处是保留了登录状态，不需要模拟登录操作，大大节约了时间。
    这种方式，也有问题存在（这个网站确实难搞），时不时会出现打码验证，但出现频率已经很低了，爬取数据多了会出现封账号的情况（大概会封一个小时）。这一个小时可以采取其他办法等一个小时后继续登陆账号。
"""