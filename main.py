import requests
from bs4 import BeautifulSoup
import fake_useragent
import csv
import pandas as pd

numbers_page = 36

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
        volume = [(v.text.split(' ')[3]) for v in soup.find_all('span', {'class': 'toogle-title'})]
        price = [(p.find('strong').text.replace(' ', '').split('р')[0]) for p in soup.find_all('span', class_='toggle btn')]
    except:
        name = 'default'
        volume = 'None'
        price = 'None'
    info = [name, volume, price]
    return info

if __name__ == "__main__":
    for l in get_links():
        info = get_info(l)

        data = dict(PRODUCT=info[0], VOLUME=info[1], PRICE=info[2])
        df = pd.DataFrame(data)
        df.to_csv(r'C:\Program Files\pythonProjects\parsing\parsing_vanille.by\price_vanille.csv',
                  sep=';', index=False, mode='a'
                  )
