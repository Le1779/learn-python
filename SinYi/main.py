import requests
from bs4 import BeautifulSoup

url = "https://www.sinyi.com.tw/tradeinfo/list/Taipei-city/106-zip/6month-dealtime/datatime-desc/2"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())
