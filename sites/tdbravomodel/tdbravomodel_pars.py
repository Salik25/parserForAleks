import numpy
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from openpyxl import load_workbook
import xlsxwriter

url_home = 'https://tdbravomebel.ru'
url = 'https://tdbravomebel.ru/catalogue/'
r = requests.get(url)
with open("index.html", "w+", encoding="utf-8") as f:
    f.write(r.text)
with open("index.html", "r", encoding="utf-8") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    cat_links = soup.find_all('div', class_='indx-col959')
    catalog_links = {}
    for i in cat_links:
        for j in i.find_all('a'):
            catalog_links[url_home + j['href']] = j.text

cat_prod_all = {}
for i in catalog_links:
    r = requests.get(i)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        content = soup.find_all('div', class_='sliders-six mt-66 tagged-category')
        for i in content:
            # print(i.find('a', class_='h-blk-title')['href'])
            try:
                r = requests.get(url_home+i.find('a', class_='h-blk-title')['href'])
                # print(url_home+i.find('a', class_='h-blk-title')['href'])
                with open("index.html", "w+", encoding="utf-8") as f:
                    f.write(r.text)
                with open("index.html", "r", encoding="utf-8") as f:
                    contents = f.read()
                    doup = BeautifulSoup(contents, 'lxml')
                    content = doup.find_all('div', class_='swiper-slide')
                    for z in content:
                        # print(z)
                        cat_prod_all[url_home + z.find('a')['href']] = z.find(
                            'span', class_='hits-prod-name-txt').text
            except AttributeError:
                for j in i.find_all('div', class_='swiper-slide five-slide-first vis-slide-five base-element'):
                    cat_prod_all[url_home + j.find('a')[
                        'href']] = j.find('span', class_='hits-prod-name-txt').text

final = {'Название позиции': [], 'Картинка': [], 'Характеристики': []}
count = 0
for i in cat_prod_all:
    r = requests.get(i)
    print(i, count)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        content = soup.find('div', class_='content-page prod-item-page prod-min-title')
        final['Название позиции'].append(content.find('h1', class_='h-cat-name-txt grad-txt').text)
        # print(content.find('div', class_='pl-col-right-mob'))
        try:
            final['Картинка'].append(
                url_home + content.find('div', class_='pl-col-right-mob').find('img')['data-src'])
        except AttributeError:
            final['Картинка'].append('-')
        final['Характеристики'].append(content.find('div', id='PROPERTIES').find('div', class_='prod-big-col prod-char-cont p8-959').text)

        # print(final)
    count += 1
df = DataFrame.from_dict(final, orient='index')
df = df.transpose()
df.to_excel('tdbravomodel.xlsx')
