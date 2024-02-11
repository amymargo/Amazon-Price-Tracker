import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import time
import csv

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

user = input('Welcome! Enter your phone number: ')
links = []
while True:
    link = input("Enter a link to add an item to your wishlist! Type 'done' when you're finished: ")
    if link == 'done':
        print('Your wishlist has been updated! You will get a text alert when the price drops 10% or more.')
        break
    else:
        links.append(link)

def get_price(dom):
    try:
        price = dom.xpath('//span[@class="a-offscreen"]/text()')[0]
        price = price.replace('$','')
        return float(price)
    except Exception as e:
        return None


def get_name(dom):
    try:
        name = dom.xpath('//span[@id="productTitle"]/text()')
        [name.strip() for name in name]
        return name[0]
    except Exception as e:
        return None

def write_to_csv(data):
    with open('master_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def get_data(link):
    try:
        response = requests.get(link, headers=header)
        soup = BeautifulSoup(response.content, 'html.parser')
        dom = et.HTML(str(soup))

        price = get_price(dom)
        product_name = get_name(dom)

        return product_name, price
    except Exception as e:
        return None, None

for link in links:
    product_name, price = get_data(link)
    data = [product_name, price, link, user]
    write_to_csv(data)
    time.sleep(1)