import requests
from bs4 import BeautifulSoup
import json
import csv
import re
import pandas as pd

headers = {
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'
}

products_url_list = []



#Собираем ссылки каждой страницы летних шин сайта:
# for i in range(1, 139):
#     url = f'https://rostov-na-donu.kolesa-darom.ru/catalog/avto/shiny/leto/nav/page-{i}/'
#     #print(url)
#     # Отправляем get запрос на нужные страницы и собираем ссылки, чтобы можно было собирать с каждой ссылки данные страницы:
#     q = requests.get(url=url)
#     result = q.content
#
#     # Извлекаем данные с получаемых страниц:
#     soup = BeautifulSoup(result, 'lxml')
#     products = soup.find_all(class_='product-card-properties__main')
#
#     #Собираем с каждой страницы ссылки на товар:
#     for product in products:
#         product_page_url = 'https://rostov-na-donu.kolesa-darom.ru' + product.get('href')
#         products_url_list.append(product_page_url)
#
#  #Сохраняем все ссылки на товар в текстовый файл:
#     with open('products_url_list.txt', 'a') as file:
#         for line in products_url_list:
#             file.write(f'{line}\n')

    ########################################################

# Открываем файл со всеми ссылками на товары и делаем так, чтобы можно было считывать с каждой ссылки инфу:
with open('products_url_list.txt') as file:
    lines = [line.strip() for line in file.readlines()]


    count = 0
    for line in lines:
        q = requests.get(line)
        result = q.content
        all_categories_dict = {}
        #Имя товара:
        soup = BeautifulSoup(result, 'lxml')
        names = soup.find(class_='product-information__title')
        all_products_names = names.text.strip()

        #Цена товара:
        price = soup.find(class_='product-price-summ')
        all_products_prices = price.text.strip() + ' ₽'

        #Ссылка на товар:
        products = soup.find_all(class_='product-card-properties__main')
        product_page_url = 'https://rostov-na-donu.kolesa-darom.ru' + line
        all_products_hrefs = product_page_url.strip()

        #print(all_products_names, all_products_prices, all_products_hrefs)

        # Сохраняем данные в таблицу. На данный момент каждое имя, цена и ссылка заменяют старую на новую.
        df = pd.DataFrame({
        'Product name': [all_products_names],
        'Product price': [all_products_prices],
        'Product link': [all_products_hrefs]
        })
        df.to_excel('Kolesa_Darom_data.xlsx')
        # Счетчик
        count += 1
        print(f'#{count}: {line} is done!')

        # all_categories_dict = [all_products_names, all_products_prices,  all_products_hrefs]
        # with open('all_categories_dict.json', 'w') as f:
        #     json.dump(all_categories_dict, f, indent=4, ensure_ascii=False)
