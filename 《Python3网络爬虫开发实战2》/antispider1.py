from selenium import webdriver
from selenium.webdriver import ChromeOptions

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)

option.add_argument('headless')

browser = webdriver.Chrome(options=option)
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
	"source": """
	Object.defineProperty(navigator, 'webdriver', {
	get: () => undefined
})"""})

browser.get('https://ssr1.scrape.center/')
print(browser.page_source)
