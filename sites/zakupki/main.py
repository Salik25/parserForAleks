import numpy
import time
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from threading import Thread
from openpyxl import load_workbook
import xlsxwriter
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}
session = requests.Session()
session.headers.update(headers)
url_home = 'https://zakupki.gov.ru'
url = 'https://zakupki.gov.ru/epz/contract/search/results.html?searchString=ремонт+дорог&morphology=on&search-filter=Дате+размещения&fz44=on&contractStageList_0=on&contractStageList=0&contractPriceFrom=10000000&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&contractDateFrom=01.01.2022&sortBy=PRICE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
catalog_page = []
final = {'Название компании': [], 'ИНН': [], 'Адрес регистрации': [], 'Телефон': [], 'E-mail': [],
             'Дата Заключение контракта': [], 'Предмет контракта': [], 'Цена контракта': []}
for i in range(1,21):
    catalog_page.append(f'https://zakupki.gov.ru/epz/contract/search/results.html?searchString=ремонт+дорог&morphology=on&search-filter=Дате+размещения&fz44=on&contractStageList_0=on&contractStageList=0&contractPriceFrom=10000000&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&contractDateFrom=01.01.2022&sortBy=PRICE&pageNumber={i}&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false')
def pars(catalog_page):
    catalog_links = {}
    for page in catalog_page:
        r = session.get(page)
        with open("index.html", "w+", encoding="utf-8") as f:
            f.write(r.text)
        with open("index.html", "r", encoding="utf-8") as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')
            cat_links = soup.find_all('div', class_='registry-entry__header-mid__number')
            for i in cat_links:
                # print(i)
                catalog_links[url_home + i.find('a')['href']] = i.text.replace(' ', '')
    # print(catalog_links)

    count = 0
    for i in catalog_links:
        # time.sleep(3)
        r = session.get(i)
        with open("index.html", "w+", encoding="utf-8") as f:
            f.write(r.text)
        with open("index.html", "r", encoding="utf-8") as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')
            content = soup.find_all('div', class_='row blockInfo')
            print(i, count)
            for j in content:
                try:
                    if j.find('h2', class_='blockInfo__title').text == 'Общие данные':
                        for z in j.find_all('section', class_='blockInfo__section section'):
                            if 'Предмет контракта' in z.text and 'Предмет контракта ' not in z.text:
                                final['Предмет контракта'].append(z.find('span', class_='section__info').text)
                            if 'Цена контракта' in z.text:
                                final['Цена контракта'].append(
                                    z.find('span', class_='section__info').text.replace('  ', '').split('\n')[0])
                            if 'Дата Заключение контракта' in z.text:
                                final['Дата Заключение контракта'].append(z.find('span', class_='section__info').text)

                    if j.find('h2', class_='blockInfo__title').text == 'Информация о поставщиках':
                        # print('find', j.find('tr', class_='tableBlock__row'))
                        index_tel = 5
                        for index, z in enumerate(j.find_all('th', class_='tableBlock__col tableBlock__col_header'), start=1):
                            if z.text == 'Телефон, электронная почта':
                                index_tel = index
                        for index, z in enumerate(j.find_all('td', class_='tableBlock__col'), start=1):
                            if index == 1:
                                final['Название компании'].append(z.text.replace('  ', ''))
                            elif index == 3:
                                final['Адрес регистрации'].append(z.text.replace('  ', ''))
                            elif index == index_tel:
                                spisok = z.text.replace('  ', '').split('\n')
                                print(spisok)
                                for pusto in spisok:
                                    if pusto == '':
                                        spisok.remove(pusto)
                                try:
                                    final['Телефон'].append(spisok[0])
                                    final['E-mail'].append(spisok[1])
                                except IndexError:
                                    pass

                            for df in z.find_all('section', class_='section'):
                                if 'ИНН:' in df.text:
                                    final['ИНН'].append(df.text.replace('ИНН:', ''))
                        # print(final)
                except AttributeError:
                    pass
        count += 1

pars(catalog_page)
df = DataFrame.from_dict(final, orient='index')
df = df.transpose()
df.to_excel('zakup.xlsx')
