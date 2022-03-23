headers = '''
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Cookie: __mta=50223769.1641693450960.1641693477938.1641698467486.6; uuid_n_v=v1; uuid=7F5C1AC070EF11EC8E83C97244BA79F359A801BB59B54A6A8F1F217AD46A4224; _csrf=f23ee575f99ee197de4ed2cd6e9d279c512d73a898b5c6404e4078731876e9de; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1641693451; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=17e3c8e12b5c8-0f2b0bb7054926-4303066-1fa400-17e3c8e12b5c8; _lxsdk=7F5C1AC070EF11EC8E83C97244BA79F359A801BB59B54A6A8F1F217AD46A4224; __mta=50223769.1641693450960.1641693466928.1641693477938.5; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1641698522; _lxsdk_s=17e3cc76c5b-e69-e46-cb2%7C%7C33
Host: www.maoyan.com
Referer: https://www.maoyan.com/films/1427538
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36
X-Requested-With: XMLHttpRequest
'''

def get_headers(header_raw):
    """
    通过原生请求头获取请求头字典
    :param header_raw: {str} 浏览器请求头
    :return: {dict} headers
    """
    return dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')


def get_cookies(cookie_raw):
    """
    通过原生cookie获取cookie字段
    :param cookie_raw: {str} 浏览器原始cookie
    :return: {dict} cookies
    """
    return dict(line.split("=", 1) for line in cookie_raw.split("; "))


