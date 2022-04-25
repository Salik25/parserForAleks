import numpy
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from openpyxl import load_workbook
import xlsxwriter

url = ['https://ekaterinburg.olmeko.ru/mebel/stoly/', 'https://ekaterinburg.olmeko.ru/mebel/kabinet/',
       'https://ekaterinburg.olmeko.ru/mebel/detskie/', 'https://ekaterinburg.olmeko.ru/mebel/spalnya/',
       'https://ekaterinburg.olmeko.ru/mebel/gostinaya/']
url_home = 'https://ekaterinburg.olmeko.ru'
catalog_links = {}
for i in url:
    r = requests.get(i)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        cat_links = soup.find_all('div', class_='col-md-4 pb-6')
        for j in cat_links:
            catalog_links[url_home + j.find('a')['href']] = j.find('span').text
print(catalog_links)

cat_prod_all = {}
for i in catalog_links:
    r = requests.get(i)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        content = soup.find_all('div', class_='bx_catalog_item double')
        if soup.find('div', class_='modern-page-navigation') != None:  # ?PAGEN_8={id}
            jk = 0
            link = ''
            for id in soup.find('div', class_='modern-page-navigation').find_all('a', class_=''):
                jk = id
                link = url_home + id['href']
                r = requests.get(link[:-1] + str(id))
                with open("index.html", "w+", encoding="utf-8") as f:
                    f.write(r.text)
                with open("index.html", "r", encoding="utf-8") as f:
                    contents = f.read()
                    soup = BeautifulSoup(contents, 'lxml')
                    content = soup.find_all('div', class_='bx_catalog_item double')
                    try:
                        for z in content:
                            cat_prod_all[url_home + z.find('div', class_='bx_catalog_item_title short_title').find('a')[
                                'href']] = z.find('div', class_='bx_catalog_item_title short_title').find('a').text
                    except AttributeError:
                        pass
        else:
            try:
                for z in content:
                    cat_prod_all[url_home + z.find('div', class_='bx_catalog_item_title short_title').find('a')[
                        'href']] = z.find('div', class_='bx_catalog_item_title short_title').find('a').text
            except AttributeError:
                pass

final = {'Категория': [], 'Название позиции': [], 'Картинка': [], 'Описание': [], 'Характеристики': [], 'Документы': [],
         'Цвет': [], 'Код': []}
count = 0
for i in cat_prod_all:
    r = requests.get(i)
    print(i, count)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        content = soup.find('div', class_='container bx-content-seection bg-white')
        final['Категория'].append(content.find('div', id='navigation').text.replace('\n', '').replace('  ', ''))
        final['Название позиции'].append(content.find('h1', class_='bx-title').text)
        final['Картинка'].append(url_home + content.find('img')['src'])
        try:
            final['Код'].append(content.find('div', class_='detailed_code').text)
        except AttributeError:
            final['Код'].append('-')
        try:
            final['Цвет'].append(content.find('div', class_='color_code').text.replace('\n', '').replace('  ', ''))
        except AttributeError:
            final['Цвет'].append('-')
        try:
            for i in content.find('div', class_='bx_item_description').find_all('dots'):
                final['Характеристики'].append(i.text)
        except AttributeError:
            final['Характеристики'].append('-')
        final['Документы'].append('-')
        try:
            for i in content.find_all('li', class_='clearfix'):
                final['Документы'][count] += i.find('div', class_='text').find('a').text + '-' + url_home + \
                                          i.find('div', class_='doc').find('a')['href'] + ' \n'
        except AttributeError:
            pass
        # print(final)
    count += 1
df = DataFrame.from_dict(final, orient='index')
df = df.transpose()
df.to_excel('olmeko.xlsx')
