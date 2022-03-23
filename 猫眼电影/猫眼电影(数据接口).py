"""
方法一：通过接口连接可以获取数据
更新：2022.1.20 -> 接口需要拖动滑块验证
"""
import requests
from fake_useragent import UserAgent


def requests_url():
    headers = {
        "User-Agent": UserAgent().random,
        # 'Host': 'www.maoyan.com',    # 不能加入这个，否者无法获取到数据！！！
        'X-Requested-With': 'XMLHttpRequest',
        # 'Referer': 'https://www.maoyan.com/films/1427538',
        # "Cookie": '__mta=50223769.1641693450960.1641693477938.1641698467486.6; uuid_n_v=v1; uuid=7F5C1AC070EF11EC8E83C97244BA79F359A801BB59B54A6A8F1F217AD46A4224; _csrf=f23ee575f99ee197de4ed2cd6e9d279c512d73a898b5c6404e4078731876e9de; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1641693451; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=17e3c8e12b5c8-0f2b0bb7054926-4303066-1fa400-17e3c8e12b5c8; _lxsdk=7F5C1AC070EF11EC8E83C97244BA79F359A801BB59B54A6A8F1F217AD46A4224; __mta=50223769.1641693450960.1641693466928.1641693477938.5; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1641698522; _lxsdk_s=17e3cc76c5b-e69-e46-cb2%7C%7C33'
               }
    url = 'https://m.maoyan.com/ajax/detailmovie?movieId=1203734'
    response = requests.get(url=url, headers=headers)
    print(response.text)


if __name__ == '__main__':
    requests_url()
