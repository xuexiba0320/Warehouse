import time
import urllib.request as request
from concurrent.futures import ProcessPoolExecutor

import pandas as pd
from selenium import webdriver


# pip install selenium==2.48.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
#  按网页url的格式生成一段时间内的日期
# get_year_months(2020, 4, 2021, 4)
# [202004, 202005, 202006, 202007, 202008, 202009, 202010, 202011, 202012, 202101, 202102, 202103, 202104]
def get_year_months(start_year, start_month, end_year, end_month):
    start_year, start_month, end_year, end_month = [int(i) for i in [start_year, start_month, end_year, end_month]]
    year_months = []
    if start_year < end_year:
        for year in range(start_year, end_year + 1):
            if year == start_year:
                if start_month > 12 or start_month < 1:
                    raise ValueError
                else:
                    for month in range(start_month, 13):
                        year_months.append(year * 100 + month)
            elif year == end_year:
                if end_month > 12 or end_month < 1:
                    raise ValueError
                else:
                    for month in range(1, end_month + 1):
                        year_months.append(year * 100 + month)
            else:
                for month in range(1, 13):
                    year_months.append(year * 100 + month)
    elif start_year == end_year:
        if start_month <= end_month:
            for month in range(start_month, end_month + 1):
                year_months.append(start_year * 100 + month)

    return year_months


if __name__ == '__main__':
    # start = time.clock()
    start = time.perf_counter()
    # ------------------------------------------基本设置-----------------------------------------------
    base_aqi_url = r'https://www.aqistudy.cn/historydata/daydata.php?'
    # city_set = ['太原', '大同', '朔州', '忻州', '阳泉', '吕梁', '晋中', '长治', '晋城', '临汾', '运城']
    city_set = ['太原']
    for k in range(0, len(city_set)):
        city_chinese_name = city_set[k]
        # 将城市中文名进行URL编码
        city_name = request.quote(city_chinese_name)
        # 拿到目标日期的月份
        year_months = get_year_months(2021, 5, 2021, 5)  # 包括最后年的最后月
        encoding = 'gbk'
        # 最大进程数
        executor_num = 10
        # ---------------------------------crawl-----------------------------------------------------------
        city_aqi_url = base_aqi_url + 'city=%s' % city_name
        start_time = time.time()
        # PhantomJS弃用，改用chrome无头
        # driver = webdriver.PhantomJS(r"C:\Users\25855\Desktop\phantomjs-2.1.1-windows\bin\phantomjs.exe")
        opt = webdriver.ChromeOptions()
        opt.add_argument('--headless')
        opt.add_argument('--disable-gpu')
        # 创建浏览器对象的时候添加配置对象
        driver = webdriver.Chrome(options=opt)

        # 这里使用多进程并行编程库里面的ProcessPoolExecutor
        with ProcessPoolExecutor(executor_num) as executor:
            for year_month in year_months:
                city_year_month_url = city_aqi_url + '&month=%d' % year_month
                # 在url中带入月份
                driver.get(city_year_month_url)
                time.sleep(1)
                # 利用pandas读取网页中的表格
                dfs = pd.read_html(driver.page_source, header=0)[0]
                time.sleep(0.5)
                dfs[1] = str(city_chinese_name)
                # 数据落地
                dfs.to_csv('selenium' + (str(city_chinese_name) + '.csv'), header=None, index=None, mode='a+',
                           encoding='utf_8_sig')
driver.quit()
end = time.perf_counter()
print('Running time: %s Seconds' % round((end - start), 2))
