import requests
import execjs
import time

def get_res(page_num,parm):
    url = 'http://match.yuanrenxue.com/api/match/1?page={}&m={}'.format(page_num,parm)
    headers = {
        'Host': 'match.yuanrenxue.com',
        'Referer': 'http://match.yuanrenxue.com/match/1',
        'User-Agent': 'yuanrenxue.project',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1641305967,1641345760; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1641305988,1641345764; qpfccr=true; no-alert3=true; tk=201454528108400921; sessionid=76poizkpnqlatcdgb5s8vg56p5br9cvk; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1641350818; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1641350821'
    }
    response = requests.get(url=url,headers=headers)
    print(response.json())
    return response.json()
#https://match.yuanrenxue.com/api/match/1?m=119b101396ac29bb22a1da0bc095ef20%E4%B8%A81641450859
                    #                       3e104b08f9ce01aa5d501a02398c81f5%E4%B8%A81641451017
def calculate_m_value():
    with open('1.js',mode='r',encoding='utf-8') as f:
        JsData = f.read()
    m_value = execjs.compile(JsData).call('get_m_value')
    m_value_process = m_value.replace("丨","%E4%B8%A8")
    print(m_value_process)
    return m_value_process


if __name__ == '__main__':
    sum_ = 0
    for page_num in range(1,6):
        print(page_num)
        time.sleep(1)
        m_value = calculate_m_value()
        res = get_res(page_num,m_value)
        for i in res['data']:
            sum_ +=i['value']
    print(sum_/50)
