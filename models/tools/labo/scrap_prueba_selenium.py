from selenium import webdriver
import time

options = webdriver.ChromeOptions()

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

url = "https://www.lapopusancristobal.com.ar/"
url = "https://www.rosario3.com/"

driver.get(url)

for a in range(10):
    print(11111)
    driver = webdriver.Chrome(options=options)
    html = driver.page_source
    print(2222)

    if "santafe" in html:
        print("1- está")
        print(html)
    else:
        print("2- no")
    driver.quit()
    print("....")
    time.sleep(1)


print("fin")