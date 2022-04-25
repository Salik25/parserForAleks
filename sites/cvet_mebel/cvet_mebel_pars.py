import numpy
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from openpyxl import load_workbook
import xlsxwriter

url_for_image = 'https://cvet-mebel.ru'

url = 'https://cvet-mebel.ru/'
r = requests.get(url)
with open("index.html", "w+", encoding="utf-8") as f:
    f.write(r.text)
with open("index.html", "r", encoding="utf-8") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    cat_links = soup.find('div', class_='catalog__menu')
    # print(cat_links)
    catalog_links = {}
    for link in cat_links.find_all('a', class_='catalog__menu-item-elem', href=True):
        if link.find('span').text.replace('\t', '') == 'Домашний текстиль\n':
            pass
        else:
            catalog_links[url + link['href']] = link.find('span').text.replace('\t', '')
    # print(catalog_links)
dict_cat_link = {}
for i in catalog_links:
    r = requests.get(i)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        chek_pages = soup.find('div', class_='pagination pagination_right')
        if chek_pages == None:
            links = soup.find_all('div', class_='product product_category js-product')
            for j in links:
                dict_cat_link[url + j.find('a', class_='product__name')['href']] = j.find('a',
                                                                                          class_='product__name').text.replace(
                    '\t', '')
        else:
            for k in chek_pages.find_all('a', class_='pagination__item'):
                count = k.text  # url+?page={i}
            for j in range(1, int(count) + 1):
                # print(i+f'?page={j}')
                r = requests.get(i + f'?page={j}')
                with open("index.html", "w+", encoding="utf-8") as f:
                    f.write(r.text)
                with open("index.html", "r", encoding="utf-8") as f:
                    contents = f.read()
                    soup = BeautifulSoup(contents, 'lxml')
                    links = soup.find_all('div', class_='product product_category js-product')
                    for z in links:
                        dict_cat_link[url + z.find('a', class_='product__name')['href']] = z.find('a',
                                                                                                  class_='product__name').text.replace(
                            '\t', '')
# print(dict_cat_link)
final = {'Категория': [], 'Название позиции': [], 'Бренд': [], 'Картинка': [], 'Описание': [], 'Объем упаковки': [],
         'Вес нетто': [], 'Цвет:': [], 'Размер': [], 'Допустимая нагрузка': [], 'Толщина столешницы': [],
         'Цвет ножек': [], 'Диаметр': [], 'Высота до сиденья': [], 'Цвет': [], 'Глубина сиденья': [], 'Цвет опор': [],
         'Страна происхождения': [], 'вес': [], 'Материал': [], 'Вес упаковки': [], 'вес брутто': [], 'Цвет  ножек': [],
         'Комплектация': [], 'Ширина': [], 'Длина': [], 'Назначение': [], 'Объем': [], 'Высота': []}
count = 0
mnoj = set()
for i in dict_cat_link:
    # print(count)
    # print(i)
    r = requests.get(i)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        content = soup.find('div', class_='main')
        categ = content.find_all('a', class_='path__item')
        final['Категория'].append(categ[-2].text)
        final['Название позиции'].append(categ[-1].text)
        try:
            final['Бренд'].append(content.find('div', class_='tovar__brand').find_next('span').text)
        except (AttributeError, TypeError):
            final['Бренд'].append('-')
        final['Картинка'].append(content.find('div', class_='tovar__image image').find_next('a')['href'])
        final['Описание'].append('')
        try:
            for h in content.find('div', class_='tabs__body tabs__body_noproduct js-body-tab2').find_all('p'):
                if 'Инструкция' in h.text:
                    pass
                else:
                    final['Описание'][count] += h.text
        except (AttributeError, TypeError):
            pass
        row = content.find_all('div', class_='features__row')
        name_row = []
        for asd in row:
            name_row.append(asd.find('div', class_='features__name').text)
        spisok = (
            'Объем упаковки', 'Вес нетто', 'Цвет:', 'Размер', 'Допустимая нагрузка', 'Толщина столешницы', 'Цвет ножек',
            'Диаметр', 'Высота до сиденья', 'Цвет', 'Глубина сиденья', 'Цвет опор', 'Страна происхождения', 'вес',
            'Материал', 'Вес упаковки', 'вес брутто', 'Цвет  ножек', 'Комплектация', 'Ширина', 'Длина', 'Назначение',
            'Объем', 'Высота')
        images_url = ''
        for z in spisok:
            if z not in name_row:
                final[z].append('-')
            elif z == 'Цвет:':
                for ghj in content.find('div', class_='features__row features__row__color').find('div',
                                                                                                 class_='features__value'):
                    if ghj.find_all('img') != None:
                        images_url = ''
                        colvo = 1
                        for jkl in ghj.find_all('img'):
                            images_url += str(colvo) + ') ' + url_for_image + jkl['src'] + ' \n'
                            colvo += 1
                        final[z].append(images_url)
            else:
                for dsfsdf in content.find_all('div', class_='features__row'):
                    if dsfsdf.find('div', class_='features__name').text == z and dsfsdf.find('div',
                                                                                             class_='features__name').text != 'Цвет:':
                        final[z].append(dsfsdf.find('div', class_='features__value').text)

        # print(final)
    count += 1

# print(mnoj)
df = DataFrame.from_dict(final, orient='index')
df = df.transpose()
df.to_excel('cvet_mebel.xlsx')
