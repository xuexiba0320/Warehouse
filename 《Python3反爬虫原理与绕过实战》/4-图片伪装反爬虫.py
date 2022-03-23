import requests
from fake_useragent import UserAgent
import pytesseract
from PIL import Image
import ddddocr


url = 'http://www.porters.vip/confusion/phonenumber.png'
headers = {
    "User-Agent": UserAgent().random,
}

response = requests.get(url=url, headers=headers).content
with open('4.png', 'wb') as f:
    f.write(response)


"""中英文识别如何切换"""
im = Image.open('4.png')
# result = pytesseract.image_to_string(im, lang='chi_sim')
result = pytesseract.image_to_string(im)
print(result)
print(len(result))


ocr = ddddocr.DdddOcr(old=True)


with open("4.png", 'rb') as f:
    image = f.read()

res = ocr.classification(image)
print(res)