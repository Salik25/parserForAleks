import numpy
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from openpyxl import load_workbook
import xlsxwriter

url = 'https://vectorpart.ru'
r = requests.get(url)
with open("index.html", "w+", encoding="utf-8") as f:
    f.write(r.text)
with open("index.html", "r", encoding="utf-8") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    cat_links = soup.find_all('div', class_='col-md-3 col-sm-3 col-xs-6 item-holder')
    catalog_links = {}
    for i in cat_links:
        catalog_links[url + i.find('a')['href']] = i.find('span', class_='abs-text').text
    print(catalog_links)

cat_prod_all = {}
for i in catalog_links:
    r = requests.get(i)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        content = soup.find_all('div', class_='item-description')
        for i in content:
            cat_prod_all[url + i.find('a')['href']] = i.find('a').text
print(cat_prod_all)

final = {'Название позиции': [], 'Картинка': [], 'Описание': [], 'Характеристики': []}
count = 0
for i in cat_prod_all:
    r = requests.get(i)
    print(i, count)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        content = soup.find('div', class_='container main-container')
        final['Название позиции'].append(content.find('h1', class_='main-heading').text)
        final['Картинка'].append(
            url + content.find('div', class_='bx_bigimages_aligner image-big-container').find('a')['href'])
        final['Описание'].append(content.find('div', class_='bx_item_description main-heading-wrapper').text)
        final['Характеристики'].append(content.find('div', class_='item_info_section').find('dl').text)

        # print(final)
    count += 1
df = DataFrame.from_dict(final, orient='index')
df = df.transpose()
df.to_excel('vector.xlsx')
