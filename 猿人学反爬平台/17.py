import requests
import httpx
# hyper
from hyper.contrib import HTTP20Adapter

headers = {'User-Agent': 'yuanrenxue.project'}
cookies="Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1641305967,1641345760; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1641305988,1641345764; qpfccr=true; no-alert3=true; tk=201454528108400921; sessionid=76poizkpnqlatcdgb5s8vg56p5br9cvk; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1641345781; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1641345857"
# (字典推导式) 将cookies字符串转换成字典
cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split("; ")}

response = 0
for i in [1,2,3,4,5]:
    url = f'https://match.yuanrenxue.com/api/match/19?page={i}'
    sessions = requests.session()
    sessions.mount('https://match.yuanrenxue.com', HTTP20Adapter())
    res = sessions.get(url, headers=headers, cookies=cookies, timeout=10)
    data = res.json()['data']  # -> list
    value = [i['value'] for i in data]
    finally_data = sum(value)
    response += finally_data

print('17题最终答案:', response)