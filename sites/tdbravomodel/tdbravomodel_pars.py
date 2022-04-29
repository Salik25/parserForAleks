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
    print(catalog_links)

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
            print(cat_prod_all, len(cat_prod_all))
#
# final = {'Название позиции': [], 'Картинка': [], 'Описание': [], 'Характеристики': []}
# count = 0
# for i in cat_prod_all:
#     r = requests.get(i)
#     print(i, count)
#     with open("index.html", "w+", encoding="utf-8") as f:
#         f.write(r.text)
#     with open("index.html", "r", encoding="utf-8") as f:
#         contents = f.read()
#         soup = BeautifulSoup(contents, 'lxml')
#         content = soup.find('div', class_='container main-container')
#         final['Название позиции'].append(content.find('h1', class_='main-heading').text)
#         final['Картинка'].append(
#             url + content.find('div', class_='bx_bigimages_aligner image-big-container').find('a')['href'])
#         final['Описание'].append(content.find('div', class_='bx_item_description main-heading-wrapper').text)
#         final['Характеристики'].append(content.find('div', class_='item_info_section').find('dl').text)
#
#         # print(final)
#     count += 1
# df = DataFrame.from_dict(final, orient='index')
# df = df.transpose()
# df.to_excel('tdbravomodel.xlsx')
