from selenium import webdriver

options = webdriver.ChromeOptions()
options.headless = True

driver = webdriver.Chrome(options=options)

url = "https://www.lapopusancristobal.com.ar/"
driver.get(url)

html = driver.page_source

print(html)

driver.quit()