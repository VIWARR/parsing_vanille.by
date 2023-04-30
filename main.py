import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json

url_vanille = 'https://vanille.by/otlivant-duhi-na-razliv?page=1'

def get_links():
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=url_vanille,
        headers={'user-agent': ua.random}
    )
    print(data.content)


if __name__ == "__main__":
    get_links()