import requests


item = {
    "name": "克里斯-保罗",
    "image": "paul.png",
    "birthday": "1985-05-06",
    "height": "185cm",
    "weight": "79.4KG"
}

url = 'http://localhost:3000'
res = requests.post(url, json=item)
print(res.text)