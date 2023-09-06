import requests
from bs4 import BeautifulSoup

url = "https://www.lapopusancristobal.com.ar/"

response = requests.get(url)

# Create a BeautifulSoup object
soup = BeautifulSoup(response.content, 'html.parser')

texto = ""

href_links = soup.find_all('img', attrs={'alt': True})
# Print the href links
for href_link in href_links:
    print(href_link['alt'])

    texto += href_link['alt'] + "\n "

print(texto)