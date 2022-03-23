import requests
from fake_useragent import UserAgent


url = 'http://www.porters.vip/verify/uas/index.html'
headers = {
    "User-Agent": UserAgent().random
}
print(headers)
response = requests.get(url=url, headers=headers).text
print(response)