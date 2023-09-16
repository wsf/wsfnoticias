from selenium import webdriver
import time
def tomar_literales_url():
    options = webdriver.ChromeOptions()


    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    url = "https://www.lapopusancristobal.com.ar/"
    url = "https://www.rosario3.com/"
    #driver.get(url)

    html = ""
    pegamos = True

    htmlset = {'1'}

    for a in range(10):

        #driver = webdriver.Chrome(options=options)
        driver.get(url)

        html_cantidato = driver.page_source

        for e in htmlset:
            if html_cantidato == e:
                pegamos = False

        htmlset.add(html_cantidato)

        if pegamos:
            html += driver.page_source
            pegamos = True

    return html

tomar_literales_url()
print("fin")