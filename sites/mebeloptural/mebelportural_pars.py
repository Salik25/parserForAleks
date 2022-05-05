import numpy
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from openpyxl import load_workbook
import xlsxwriter

url_home = 'https://mebeloptural.ru/'
url = 'https://mebeloptural.ru/allcat'
r = requests.get(url)
with open("index.html", "w+", encoding="utf-8") as f:
    f.write(r.text)
with open("index.html", "r", encoding="utf-8") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    cat_links = soup.find('div', class_='container-right').find_all('a')
    catalog_links = {}
    for i in cat_links:
        catalog_links[url_home + i['href']] = i.text.replace('\t', '')
    # print(catalog_links)

cat_prod_all = {}
for i in catalog_links:
    r = requests.get(i)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        content = soup.find('div', class_='container-right')
        # ?page={id}
        if soup.find('div', class_='pagination pagination_right') != None:  # ?PAGEN_8={id}
            jk = 0
            link = ''
            for id in soup.find('div', class_='pagination pagination_right').find_all('a'):
                jk = id.text
                link = url_home + id['href']
                r = requests.get(link[:-1] + str(id))
                with open("index.html", "w+", encoding="utf-8") as f:
                    f.write(r.text)
                with open("index.html", "r", encoding="utf-8") as f:
                    contents = f.read()
                    soup = BeautifulSoup(contents, 'lxml')
                    content = soup.find_all('div', class_='product product_3x js-product')
                    try:
                        for z in content:
                            cat_prod_all[url_home + z.find('a', class_='product__name')[
                                'href']] = z.find('a', class_='product__name').text.replace('\t', '')
                    except AttributeError:
                        pass
        else:
            try:
                content = soup.find_all('div', class_='product product_3x js-product')
                for z in content:
                    cat_prod_all[url_home + z.find('a', class_='product__name')[
                        'href']] = z.find('a', class_='product__name').text.replace('\t', '')
            except AttributeError:
                pass
print(len(cat_prod_all))

final = {'Категория': [], 'Название позиции': [], 'Картинка': [], 'Описание': []}
count = 0
for i in cat_prod_all:
    r = requests.get(i)
    print(i, count)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        content = soup.find('div', class_='main')
        final['Название позиции'].append(content.find('h1', itemprop='name').text)
        final['Категория'].append(content.find('div', class_='path').text)
        final['Картинка'].append(content.find('img', itemprop='image')['src'])
        final['Описание'].append(content.find('div', class_='productpage__description').text)
        # print(final)
    count += 1
df = DataFrame.from_dict(final, orient='index')
df = df.transpose()
df.to_excel('mebelportural.xlsx')
