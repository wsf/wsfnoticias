from selenium import webdriver

options = webdriver.ChromeOptions()

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

url = "https://www.lapopusancristobal.com.ar/"
driver.get(url)

html = driver.page_source

print(html)

driver.quit()