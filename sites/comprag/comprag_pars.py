import numpy
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from openpyxl import load_workbook
import xlsxwriter

count = 0

url = 'https://www.comprag.ru/'
final = {'Категория': [], 'Название позиции': [], 'Картинка': [], 'Описание': [], 'Характеристики': [], 'Документы': []}
r = requests.get(url)
with open("index.html", "w+", encoding="utf-8") as f:
    f.write(r.text)
with open("index.html", "r", encoding="utf-8") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    cat_links = soup.find('div', class_='maincat').find_all('div', class_='item')
    catalog_links = {}
    for link in cat_links:
        catalog_links[url + link.find('a')['href']] = link.find('div', class_='ttl').text
# print(catalog_links)
dict_cat_link = {}
for i in catalog_links:
    r = requests.get(i)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        links = soup.find_all('div', class_='contbgtop')
        # TODO найти похожесть между тремя паттернами страниц. как можно получтаь все ссылки со всех видов
        for j in links:
            dict_cat_link[url + j.find('a')['href']] = j.find('div', class_='ttl').text
# print(dict_cat_link)
tovar_cat_links = {}
for i in dict_cat_link:
    r = requests.get(i)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        content = soup.find_all('div', class_='item contbgbot')
        if content != None:
            for j in content:
                tovar_cat_links[url + j.find('a')['href']] = j.find('div', class_='ttl').text
        else:
            # записать в ексел
            content = soup.find('div', class_='body')
            print(content)
            final['Категория'].append(content.find('div', class_='pgttl topgrad').find_next('h1').text)
            final['Название позиции'].append(content.find('div', class_='content topgrad').find_next('h2').text)
            final['Картинка'].append(url + content.find('table', class_='anons').find_next('img')['src'])
            final['Описание'].append(content.find('table', class_='anons').find_next('p').text)
            try:
                final['Описание'][count] += content.find('div', class_='contbgbot marbot10').text
                final['Описание'][count] += content.find('div', class_='plaw').text
                final['Описание'][count] += content.find('table', class_='graytext pad20 graf').text
            except (AttributeError, TypeError):
                pass
            final['Характеристики'].append(content.find('table', class_='thtbl').text)
            doc = ''
            if content.find('div', class_='contbgtop pad20') != None:
                for i in content.find_all('div', class_='dwl'):
                    # print(i.find('span', class_="product-item-detail-files-docs-name").text)
                    doc += i.find('div', class_="txt").text + ' - ' + url + i.find('a')['href'] + ' \n'
            final['Документы'].append(doc)
# print(tovar_cat_links)

for i in tovar_cat_links:
    r = requests.get(i)
    print(count)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        content = soup.find('div', class_='body')
        final['Категория'].append(content.find('div', class_='pgttl topgrad').find_next('h1').text)
        final['Название позиции'].append(content.find('div', class_='content topgrad').find_next('h2').text)
        final['Картинка'].append(url + content.find('table', class_='anons').find_next('img')['src'])
        final['Описание'].append(content.find('table', class_='anons').find_next('p').text)
        try:
            final['Описание'][count] += content.find('div', class_='contbgbot marbot10').text
            final['Описание'][count] += content.find('div', class_='plaw').text
            final['Описание'][count] += content.find('table', class_='graytext pad20 graf').text
        except (AttributeError, TypeError):
            pass
        try:
            final['Характеристики'].append(content.find('table', class_='thtbl').text)
        except (AttributeError, TypeError):
            final['Характеристики'].append('-')
        doc = ''
        if content.find('div', class_='contbgtop pad20') != None:
            for j in content.find_all('div', class_='dwl'):
                # print(i.find('span', class_="product-item-detail-files-docs-name").text)
                doc += j.find('div', class_="txt").text + ' - ' + url + j.find('a')['href'] + ' \n'
        final['Документы'].append(doc)
        # print(final)
        print(i)
    count += 1
df = DataFrame.from_dict(final, orient='index')
df = df.transpose()
df.to_excel('comprag.xlsx')
