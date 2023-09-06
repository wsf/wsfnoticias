from selenium import webdriver

driver = webdriver.Chrome()
url = "https://www.lapopusancristobal.com.ar/"
driver.get(url)

html = driver.page_source

print(html)

driver.quit()