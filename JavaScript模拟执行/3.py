import requests
from playwright.sync_api import sync_playwright

base_url = 'https://spa2.scrape.center'
index_url = base_url + '/api/movie?limit={limit}&offset={offset}&token={token}'
LIMIT = 10
max_page = 10

context = sync_playwright().start()
browser = context.chromium.launch()
page = browser.new_page()
page.route(
    '/js/chunk-10192a00.243cb8b7.js',
    lambda route: route.fulfill(path='3.js')
)
page.goto(base_url)


def get_token(offset):
    result = page.evaluate('''() => {
                return window.encrypt("%s","%s")
                }''' % ('/api/movie', offset)
                )
    return result


for i in range(max_page):
    offset = i * LIMIT
    token = get_token(offset)
    index_url = index_url.format(limit=LIMIT, offset=offset, token=token)
    print(index_url)
    response = requests.get(index_url)
    print(response.json())
