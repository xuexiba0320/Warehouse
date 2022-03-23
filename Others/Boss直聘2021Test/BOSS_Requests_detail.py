"""
Boss直聘
cookie失效快，能否通过js模拟生成随机cookie值？？ cookie的基本知识和原理？？？
发送get请求添加cookie的方式？？？ https://www.cnblogs.com/dai-zhe/p/14828019.html， 2021-12-28 做笔记！！！
"""
import requests
from lxml import etree
from fake_useragent import UserAgent


class Boss(object):
    def __init__(self):
        # keyword = input('请输入需要查找的岗位:')
        ua = UserAgent().random
        self.keyword = 'python爬虫'
        self.url = 'https://www.zhipin.com/job_detail/a7ecf884d333ce151nF52NW9FVNX.html'
        self.headers = {
            'Cookie': 'lastCity=100010000; wd_guid=24c75d03-5533-4b25-a81d-e334846d2997; historyState=state; __zp_seo_uuid__=7a9788f8-1853-4b69-a29b-14324e22eb29; sid=sem; __g=sem; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1640788202,1640857753,1641103021,1641107199; acw_tc=0b6e704a16411318903067611e01a81f3f6ca75533f1681bcf6eca28d994b6; __c=1641103022; __l=r=https%3A%2F%2Fwww.baidu.com%2Fbaidu.php%3Furl%3D0f00000uEDLSpLgiCC37rEe2ujOYGQfOCBiOIftHcLjdp_MQHD8i7AN8KlxITMV7xJ6hvt4UQz_gi46-lYaYPOAaI8STqkrBTr5S6_A0DpGDRByDfnvoifEyJMpKMg_yojDTKtMFKPmR13TJv9TTykgczqCXcmApMvWI-KX1WTvoQHEqwFS4iG53u54OeBjsCQk43LlcpEJ7ionrs7V3alyKvWTs.DD_NR2Ar5Od663rj6t8AGSPticrKMASj9k_k86EukmccYlxSQFLeRlrKYd1A1IkvyUPMHv2N9h9mLvIrqf.U1Yk0ZDqmhq1TsKspynqn0KY5yFETLn0pyYqnWcd0ATqTZPYT6KdpHdBmy-bIfKspyfqP0KWpyfqrjf0UgfqnH0krNtknjDLg1DsnWPxnW0dnNt1nHcYg1nsnjFxn1msnfKopHYs0ZFY5HRsnfKBpHYkPH9xnW0Yg1RsnsKVm1YknjD4g1D4nHbznjTkrjwxnH0zndtznjRkg1Dsn-tknjFxn0KkTA-b5H00TyPGujYs0ZFMIA7M5H00mycqn7ts0ANzu1Ys0ZKs5H00UMus5H08nj0snj0snj00Ugws5H00uAwETjYs0ZFJ5H00uANv5gKW0AuY5H00TA6qn0KET1Ys0AFL5HDs0A4Y5H00TLCq0A71gv-bm1dsTzdMXh410A-bm1dcHbD0TA9YXHY0IA7zuvNY5Hm1g1KxnHRs0ZwdT1YknWD1n1n1nWfkn1mdPWnLrjf1nfKzug7Y5HDvPjDknjTkrHRYPHf0Tv-b5H6duyf4mH0snj0snhckuHR0mLPV5HDsnWn4PHNAfRFAnYwDPH60mynqnfKsUWYs0Z7VIjYs0Z7VT1Ys0ZGY5H00UyPxuMFEUHYsg1Kxn7tsg1KxnH0YP-ts0Aw9UMNBuNqsUA78pyw15HKxn7tsg1KxPjnknjb4PNtYn1DsrHbdg100TA7Ygvu_myTqn0Kbmv-b5H00ugwGujYVnfK9TLKWm1Ys0ZNspy4Wm1Ys0Z7VuWYs0AuWIgfqn0KGTvP_5H00mywhUA7M5HD0UAuW5H00uAPWujY0IZF9uARqP1msnW0z0AFbpyfqnRujwjf3nDFKnDFjnbf4wWwafHc1nj7APH0LPjw7PWm0UvnqnfKBIjYs0Aq9IZTqn0KEIjYk0AqzTZfqninsc1Dsc1cWn1fvnHb1nHnsc10Wna3snj0snj0Wninzc10WQinsQW0znj0snankQW0snjDsn0K3TLwd5Hc4PjcsnWTd0Z7xIWYsQW6dg108njKxna3sn7tsQW6sg108P19xni3sn7tsQWDLg100mMPxTZFEuA-b5H00ThqGuhk9u1Ys0APv5fKGTdqWTADqn0KWTjYs0AN1IjYs0APzm1Yvn1b3r0%26us%3Dnewvui%26xst%3DmWYkwbPDPj6sfbDsfbnzwj-APDFKnWnsnRmdnjTYPDRvP6715HbvPH0dn164njD1nHRvrHRsP1IxnWcdg10KI1dBULP10gDqmhq1Ts7d5Hc4PjcsnWTd0gfqnHmYnHDsP1D4Pf7VTHYs0W0aQf7Wpjdhmdqsms7_IHYs0yP85yF9pywd0HckPWf1nHndPWT%26word%3D%26ck%3D5381.2.122.283.184.255.287.173%26shh%3Dwww.baidu.com%26sht%3Dbaidu%26wd%3D%26bc%3D110101&l=%2Fwww.zhipin.com%2Fjob_detail%2Fa7ecf884d333ce151nF52NW9FVNX.html&s=3&g=%2Fwww.zhipin.com%2F%3Fkeyword%3D853808864%26bd_vid%3D7338381891090644526%26sid%3Dsem%26_ts%3D1641107198037&friend_source=0&s=3&friend_source=0; __a=25641414.1640667794.1640857753.1641103022.108.4.13.6; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1641132091; __zp_stoken__=4ddadKQEhWRB%2Fdz5dbVJBKmwRbD9TFx4dRD8BFRwaRUN1R3M4VxEPZyxFIQZ3XCllPBx0OlcfVQBEJH83ERsiLhp%2BJi06S0J1ET5XeChEPj5nezAWJkd%2BVz1TT30mOhgufiVGTgw%2FdgV4ZXo%3D',
            'User-Agent': ua,
            'Host': 'www.zhipin.com'
        }

    def request_url(self):
        response = requests.get(url=self.url, headers=self.headers)
        return response.text

    @staticmethod
    def parse(response):
        data = etree.HTML(response)
        describe = data.xpath('//*[@id="main"]//div[@class="detail-content"]/div[@class="job-sec"]/div/text()')
        # describe = describe.strip()
        print(describe)
        print(len(describe))
        # for data in describe:
        #     print(data)
        # return describe

    @staticmethod
    def save(data):
        print('保存数据！！')

    def main(self):
        response = self.request_url()
        data = self.parse(response)
        self.save(data)


if __name__ == '__main__':
    Boss = Boss()
    Boss.main()
