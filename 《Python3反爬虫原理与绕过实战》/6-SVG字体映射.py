import requests
from fake_useragent import UserAgent


url = 'http://www.porters.vip/verify/cookie/content.html'
headers = {
    "User-Agent": UserAgent().random,
    'Cookie': 'isfirst=789kq7uc1pp4c'
}
print(headers)
response = requests.get(url=url, headers=headers).text
print(response)