import numpy
import time
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from openpyxl import load_workbook
import xlsxwriter

url_home = 'https://legion-tehno.ru'
catalog_links = {}
for i in range(1, 10):
    url = f'https://legion-tehno.ru/catalog/okrasochnoe-oborudovanie-graco/?PAGEN_1={i}'
    r = requests.get(url)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        cat_links = soup.find_all('div', class_='col-xs-6 col-md-3')
        for j in cat_links:
            catalog_links[url_home + j.find('div', class_='product-item-title').find('a')['href']] = j.find('div',
                                                                                                            class_='product-item-title').text
# print(catalog_links)
# print(len(catalog_links))
final = {'Название позиции': [], 'Категория': [], 'Картинка': [], 'Описание': [], 'Характеристики': [], 'Документы': []}
count = 0
for i in catalog_links:
    print(count)
    time.sleep(1)
    r = requests.get(i)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        content = soup.find('div', class_='page-container-wrapper')
        final['Название позиции'].append(content.find('h1', id='pagetitle').text)
        final['Картинка'].append(
            'https:' + content.find('div', class_='product-item-detail-slider-image active').find('img')[
                'data-lazyload-src'])
        final['Категория'].append(content.find('div', class_='navigation-items').select_one(
            'div:last-child > a > span[itemprop="name"]').get_text())
        if content.find('div', class_='col-xs-12 product-item-detail-description') != None:
            final['Описание'].append(content.find('div', class_='col-xs-12 product-item-detail-description').text)
        else:
            final['Описание'].append('-')
        final['Характеристики'].append(content.find('div', class_='product-item-detail-properties-container').text)
        doc = ''
        if content.find('div', class_='row product-item-detail-files-docs') != None:
            for i in content.find('div', class_='row product-item-detail-files-docs').find_all('a'):
                print(i.find('span', class_="product-item-detail-files-docs-name").text)
                doc += i.find('span', class_="product-item-detail-files-docs-name").text + ' - ' + url_home + i[
                    'href'] + ' \n'
        final['Документы'].append(doc)
        # print(final)
    count += 1
print(count)
df = DataFrame.from_dict(final, orient='index')
df = df.transpose()
df.to_excel('legion.xlsx')
