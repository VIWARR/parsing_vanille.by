import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json

url_vanille = 'https://vanille.by/otlivant-duhi-na-razliv?page=35'

def get_links():
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=url_vanille,
        headers={'user-agent': ua.random}
    )

    if data.status_code != 200:
        return

    soup = BeautifulSoup(data.content, 'lxml')
    try:
        page_count = int(soup.find('div', {'class': 'content__flex-container'}).find_all('li')[-1].find('span').text)
    except:
        return
    print(page_count)


if __name__ == "__main__":
    get_links()