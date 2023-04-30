import requests
from bs4 import BeautifulSoup
import fake_useragent
import json

numbers_page = 35

def get_soup(number):
    ua = fake_useragent.UserAgent()
    response = requests.get(
        url=f'https://vanille.by/otlivant-duhi-na-razliv?page={number}',
        headers={'user-agent': ua.random}
    )
    if response.status_code != 200:
        return
    soup = BeautifulSoup(response.content, 'lxml')
    return soup


def get_links():
    soup = get_soup(numbers_page)
    try:
        page_count = int(soup.find('div', {'class': 'content__flex-container'}).find_all('li')[-1].find('span').text)
    except:
        return

    for page in range(page_count):
        try:
            soup = get_soup(page)
            for link in soup.find_all('a', {'class': 'product-cut__title-link'}):
                yield f"https://vanille.by{link.attrs['href']}"
        except Exception as q:
            print(f'{q}')

def get_info(link):
    ua = fake_useragent.UserAgent()
    response = requests.get(
        url=link,
        headers={'user-agent': ua.random}
    )
    if response.status_code != 200:
        return
    soup = BeautifulSoup(response.content, 'lxml')

    try:
        name = soup.find('h1', 'product-intro__title').text
        volume = soup.find('span', {'class': 'toogle-title'}).find('span').text
        price = soup.find('strong').text
    except:
        name = 'default'
        volume = 'None'
        price = 'None'
    info = [name, volume[0], price.split('р')[0]]

    return info

if __name__ == "__main__":
    for l in get_links():
        print(get_info(l))