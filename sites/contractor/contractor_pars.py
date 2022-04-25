import numpy
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from openpyxl import load_workbook
import xlsxwriter


url = 'https://www.contracor.ru'
r = requests.get(url)
with open("index.html", "w+", encoding="utf-8") as f:
    f.write(r.text)
with open("index.html", "r", encoding="utf-8") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    cat_links = soup.find('td', class_='catalog')
    catalog_links = {}
    for link in cat_links.find_all('a', href=True):
        catalog_links[url + link['href']] = str(link)[str(link).rfind('"') + 2:str(link).rfind('<')]
    print(catalog_links)
dict_cat_link = {}
for i in catalog_links:
    r = requests.get(i)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        links = soup.find('td', class_='content').select('tr a')
        # TODO найти похожесть между тремя паттернами страниц. как можно получтаь все ссылки со всех видов
        for j in links:
            if j['href'][:2] == '..':
                dict_cat_link[i[:i[:i.rfind('/')].rfind('/')] + j['href'][2:]] = str(j)[
                                                                                 str(j).find('>') + 1:str(j).rfind('<')]
            elif j['href'][:15] == '/documentations':
                dict_cat_link[i] = catalog_links[i]
            elif j['href'][0] == '/':
                dict_cat_link[url + j['href']] = str(j)[str(j).find('>') + 1:str(j).rfind('<')]
            else:
                dict_cat_link[i[:i.rfind('/') + 1] + j['href']] = str(j)[str(j).find('>') + 1:str(j).rfind('<')]
# print(dict_cat_link)
final = {'Категория': [], 'Название позиции': [], 'Картинка': [], 'Описание':[],'Характеристики': [],
         'Информация для заказа': []}
count = 0
for i in dict_cat_link:
    r = requests.get(i)
    with open("index.html", "w+", encoding="utf-8") as f:
        f.write(r.text)
    with open("index.html", "r", encoding="utf-8") as f:
        contents = f.read()
        spis = ["ТЕХНИЧЕСКИЕ ХАРАКТЕРИСТИКИ","ИНФОРМАЦИЯ ДЛЯ ЗАКАЗА",'ХАРАКТЕРИСТИКИ']
        soup = BeautifulSoup(contents, 'lxml')
        content = soup.find('td', class_='content')
        final['Категория'].append(content.find(class_='mainttl').text)
        final['Название позиции'].append(content.find('span', class_='docsttl').text)
        final['Картинка'].append(url + content.find('p').find_next('img')['src'])
        final['Описание'].append('')
        try:
            final['Описание'][count] += content.find('span', class_='docsttl').find_next('p').text
        except (AttributeError,TypeError):
            pass
        final['Характеристики'].append('-')
        final['Информация для заказа'].append('-')
        for l in content.find_all(class_='subttl'):
            if l.text != None:
                if l.text not in spis:
                    final['Описание'][count] += l.find_next('p').text
                elif l.text == "ТЕХНИЧЕСКИЕ ХАРАКТЕРИСТИКИ":
                    final['Характеристики'][count] = l.find_next('table').text
                elif l.text == 'ХАРАКТЕРИСТИКИ':
                    final['Характеристики'][count] = l.find_next('p').text
                elif l.text == "ИНФОРМАЦИЯ ДЛЯ ЗАКАЗА":
                    final['Информация для заказа'][count] = l.find_next('table').text

        # print(final)
    count +=1
df = DataFrame.from_dict(final, orient='index')
df = df.transpose()
df.to_excel('contractor.xlsx')
