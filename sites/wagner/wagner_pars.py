import numpy
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from openpyxl import load_workbook
import xlsxwriter

url_for_image = 'https://wagner.ru'
url = 'https://wagner.ru/professionalnoe/products/stroitelstvo'
r = requests.get(url)
with open("index.html", "w+", encoding="utf-8") as f:
    f.write(r.text)
with open("index.html", "r", encoding="utf-8") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    cat_links = soup.find('div', class_='row mx-0')
    catalog_links = {}
    for link, names in zip(cat_links.find_all('a', href=True), cat_links.find_all('h3', class_='text-mineShaft')):
        catalog_links[url + link['href']] = names.text
    print(catalog_links)
final = {'Название позиции': [], 'Картинка': [], 'Описание': [], 'Характеристики': []}
count = 0
for i in catalog_links:
    r = requests.get(i)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        spis = ["ТЕХНИЧЕСКИЕ ХАРАКТЕРИСТИКИ", "ИНФОРМАЦИЯ ДЛЯ ЗАКАЗА", 'ХАРАКТЕРИСТИКИ']
        soup = BeautifulSoup(contents, 'lxml')
        content = soup.find('section', class_='content-wrapper bg-white mx-auto product-detail-page')
        final['Название позиции'].append(content.find('h1').text)
        final['Картинка'].append(url_for_image + content.find('a', class_='js-product-image-link')['href'])
        stringa = soup.select('div>div>div>div>div>div>div>ul>li')
        stroka = ''
        for i in stringa:
            stroka += i.get_text()
        stroka += content.find('div', id='description').text
        final['Описание'].append(stroka)
        final['Характеристики'].append(content.find('div', id='technical-data').text)


        # print(final)
    count += 1
print(count)
df = DataFrame.from_dict(final, orient='index')
df = df.transpose()
df.to_excel('wagner.xlsx')
