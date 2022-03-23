"""
2021.01-02
"""
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from fake_useragent import UserAgent
from lxml import etree
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import random
import IP_Testing02


class Boss(object):
    def __init__(self):
        """
        --> initialization parameter
        --> Configuring the Browser
        """
        self.ua = UserAgent()

        self.keyword = 'python爬虫'
        self.url = 'https://www.zhipin.com/c100010000/?query={0}&ka=sel-city-100010000'.format(self.keyword)
        """浏览器配置"""
        # 实例化一个ChromeOptions对象,需导入 from selenium.webdriver import ChromeOptions
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--user-agent=' + self.ua.random)
        self.options.add_argument('--log-level=3')
        # 启动时窗口最大化
        self.options.add_argument('--start-maximized')
        # 关闭浏览器左上方 ’Chrome正在受到自动测试软件控制‘ 的提示
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 循环开始、停止标志
        self.mark = True
        self.cookie = 'lastCity=100010000; wd_guid=24c75d03-5533-4b25-a81d-e334846d2997; historyState=state; __zp_seo_uuid__=c8e18f88-c76f-4bd0-bc90-ea04ccc56d22; sid=sem; __g=sem; __l=r=https%3A%2F%2Fwww.baidu.com%2Fbaidu.php%3Furl%3D060000KKXYb9K48fS4Q06f2NdXG0KtSQTBeDoUNR7ypKHb1F10U1aLKiEy5gg1Nq2KDho1ATk7JE7vyrvgAIespkli8wq2JzVeaKR5QG3f7SgyqUE5wIFtUgroaTgsaJ_vFBgRZ6LWnn0RC44CnunVG7wKX14S26wJfAwG77GFvhS_P2ujZimqM3M4eosPZCB0WqeD6V9tDyGB7AsCBxxudWwGwh.DD_NR2Ar5Od663rj6t8AGSPticrKMASj9k_k86EukmccYlxSQFLeRlrKYd1A1IkvyUPMHv2N9h9mLvIrqf.U1Yk0ZDqmhq1TsKspynqn0KY5yFETLn0pyYqnWcd0ATqTZPYT6KdpHdBmy-bIfKspyfqP0KWpyfqrjf0UgfqnH0krNtknjDLg1DsnWPxnW0dnNt1nHcYg1nsnjFxn1msnfKopHYs0ZFY5HRsnfKBpHYkPH9xnW0Yg1RsnsKVm1Ykrjm1nHTzPWRzg1D4nHbznjTkrjwxnH0zndtznjRkg1Dsn-tknjFxn0KkTA-b5H00TyPGujYs0ZFMIA7M5H00mycqn7ts0ANzu1Ys0ZKs5H00UMus5H08nj0snj0snj00Ugws5H00uAwETjYs0ZFJ5H00uANv5gKW0AuY5H00TA6qn0KET1Ys0AFL5HDs0A4Y5H00TLCq0A71gv-bm1dsTzdMXh93XfKGuAnqiD4K0ZKCIZbq0Zw9ThI-IjYvndtsg1Ddn0KYIgnqnHckn1n1n1cYnHnvPHm1P16Yn1D0ThNkIjYkPWfknHTvnHmvn1fd0ZPGujY4PW6vmWTznW0snjcvPWms0AP1UHYzPWDdPHRvrjFKwbRsPWR10A7W5HD0TA3qn0KkUgfqn0KkUgnqn0KlIjYs0AdWgvuzUvYqn7tsg1Kxn7tsg1DsPjuxn0Kbmy4dmhNxTAk9Uh-bT1Ysg1Kxn7tsg1f1nH04rHNxPjnknjb4PNts0ZK9I7qhUA7M5H00uAPGujYs0ANYpyfqQHD0mgPsmvnqn0KdTA-8mvnqn0KkUymqn0KhmLNY5H00pgPWUjYs0A7buhk9u1Yk0Akhm1Ys0AwWmvfq0Zwzmyw-5HTvnjcsn6KBuA-b5H7AfYfYrjKafHKaf1FDrRmYfbDzn10kwWRsP1fYwHmv0AqW5HD0mMfqn0KEmgwL5H00ULfqnfKETMKY5HDWnanknanzc1nYPWD4n1D1nansc108nj0snj0sc1DWnBnsczYWna3snW0snj0Wni3snj0knj00XZPYIHYzrHfznjcLPfKkgLmqna33PNtsQW0sg108njKxna33rNtsQWT4g1D8njKxna3kPdts0AF1gLKzUvwGujYs0ZFEpyu_myTqn0KWIWY0pgPxmLK95H00mL0qn0K-TLfqn0KWThnqn1TYrjc%26us%3Dnewvui%26xst%3DmWYkwbPDPj6sfbDsfbnzwj-APDFKnWnsnRmdnjTYPDRvP6715HDsrjfvPHR3nH04nWcdn1fvPWRvg1czPNts0gTqmhq1Ts7k5yFETLnKIHYzrHfznjcLPf7Y5HDvPjDkP1mkPWmKUgDqn0cs0BYKmv6quhPxTAnKUZRqn07WUWdBmy-bIfDdrjc4PHTzPWn%26word%3D%26ck%3D8193.2.125.284.187.676.202.272%26shh%3Dwww.baidu.com%26sht%3Dbaidu%26wd%3D%26bc%3D110101&l=%2Fwww.zhipin.com%2F%3Fkeyword%3D853808864%26bd_vid%3D8222261108418415717%26sid%3Dsem%26_ts%3D1641176168916&s=3&g=%2Fwww.zhipin.com%2F%3Fkeyword%3D853808864%26bd_vid%3D8222261108418415717%26sid%3Dsem%26_ts%3D1641176168916&friend_source=0&s=3&friend_source=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1641103021,1641107199,1641176171,1641176220; __c=1641176171; __a=25641414.1640667794.1641103022.1641176171.144.5.35.35; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1641181029; __zp_stoken__=6d98dZxpyJHoxZk9UK2lRCFJ7bHFXSy8DaC1FPX1rdmdCalBsC0JyDWJUNS8jcXBHAnZ0dExMe0wKSCUffQl8OyNKeVshDgQ%2BHBISUEl%2FDXIhETAyYSECbXNCC1VHDCsMQE9GABdsC282dD4%3D'
        self.data_list = []

    def set_options(self):
        ip_port = IP_Testing02.run()  # IP获取接口
        # proxy = {'http': ip_port, 'https': ip_port, }
        self.options.add_argument('--proxy-server=http://{0}'.format(ip_port))
        self.driver = webdriver.Chrome(options=self.options)

    def open_browser(self):
        """open the browser"""
        # 每打开一次浏览器更换一次IP地址
        self.set_options()
        # 启动浏览器
        self.driver.get(self.url)
        # self.driver.get("http://www.baidu.com")

    def next_page(self):
        """click next page"""
        count = 0
        num = 0
        while True:
            time.sleep(random.randint(1, 6))
            count += 1
            try:
                self.parse()
            except Exception as e:
                pass
            else:
                try:
                    # 显性等待出现下一页出现并可以点击 最后下一页无法点击，等待5s后报出异常，try中的except接收异常然后将剩余的几页数据吧保存
                    WebDriverWait(self.driver, 15, 1).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[@class="page"]/a[@class="next"]')))
                    self.driver.find_element(By.XPATH, '//div[@class="page"]/a[@class="next"]').click()
                except Exception as e:
                    print('一共{}条数据！！'.format(len(self.data_list)))
                    break
                else:
                    print("正在爬取第{}页数据".format(count))
                    # pass
                    # 测试：设置只爬取一页
                    if count == 1:
                        break

    def parse(self):
        """parse data -> one page"""
        time.sleep(1)
        page = self.driver.page_source   # the type of page_source  -> str
        xp = etree.HTML(page)
        self.cookie = self.driver.get_cookies()
        dataset = xp.xpath('//div[@id="main"]//div[@class="job-list"]/ul/li')
        # print(len(dataset))
        for data in dataset:
            link = data.xpath('.//span[@class="job-name"]/a/@href')[0]
            # print(title, area, company, salary, link)
            url = 'https://www.zhipin.com' + link
            self.data_list.append(url)

    def save(self):
        """怎么爬取一定数据就保存起来(不能覆盖之前的)，而不是爬取完才保存？？"""

        """保存到文件中"""
        """保存到MySQL数据库中"""

        return self.data_list

    def cookies(self):
        """定时获取Cookies值"""
        # 打开浏览器,随机打开一个url获取cookie
        self.driver.get(url=random.choice(self.data_list))
        # 获取cookie值
        cookies = self.driver.get_cookies()
        # 关闭浏览器
        self.driver.close()
        # 返回cookies值
        return cookies

    def requests_url(self):
        """
        使用requests向详情页发起请求需要携带cookie值才能获取数据
        解决cookie失效快：selenium在翻译的时候获取多个cookie（cookie）？然后传给requests发起get请求？？
        2021-12-29：先验证一个cookie可以使用多长时间 or 一个cookie可以发起多少次请求
        """
        print(self.data_list)  # 检测是否拿到岗位url列表
        print(self.cookie)
        # 设置定时任务，定时打开浏览器获取cookie
        # cookie = self.cookies()
        headers = {
                   "user-agent": self.ua.random,
                   "Accept-Encoding": "gzip,deflate,br",
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   "Host": 'www.zhipin.com',
                   "Connection": "keep-alive",
                   "Cookie": self.cookie
                }
        # headers = {"headers": self.ua.random}
        url_list = self.save()

        # 使用代理IP
        ip_port = IP_Testing02.run()  # IP获取接口
        proxy = {'http': ip_port, 'https': ip_port, }

        for url in url_list:
            """meta name="keywords"""
            # try:
            response = requests.get(url=url, headers=headers, proxies=proxy, stream=True)
            data = etree.HTML(response.text)
            # 判断能否成功访问网页（元素判断）,没有匹配到则为【】，len(judge)==0 --> False
            judge = data.xpath('//meta[@name="keywords"]')
            print(len(judge))
            # 元素存在，成功访问到页面数据
            if len(judge) > 0:
                describe = data.xpath('//*[@id="main"]//div[@class="detail-content"]/div[@class="job-sec"]/div/text()')
                print(describe)
            else:
                print('爬取失败1')
            # except Exception as e:
            #     print('爬取失败2')



    def main(self):
        """main function"""
        """出现问题就更换ip重新打开浏览器，记住页数继续运行"""
        # self.open_browser()  # 只能调用一次！！！打开浏览器第一次url就ok
        # # time.sleep(2)
        # # 点击下一页获取数据
        # self.next_page()
        #
        # if not self.mark:
        #     # 没有异常就退出循环
        #     break
        # elif self.mark:
        #     # close browser
        #     self.driver.quit()
        #     # 有异常重新打开浏览器运行
        #     continue
        self.open_browser()  # 只能调用一次！！！打开浏览器第一次url就ok
        # time.sleep(2)
        # 点击下一页获取数据
        self.next_page()
        self.driver.quit()

        # 得到全部url数据，发起详情页requests请求
        self.requests_url()


if __name__ == '__main__':
    Boss = Boss()
    Boss.main()


