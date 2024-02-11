import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import pandas as pd
from twilio.rest import Client
import sys
import csv

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

account_sid = 'AC20cd1824c8d8f0d0e45989bfba4ae034'
auth_token = '443cdfc15c45a876427ea7ae449428c8'
def read_links_from_csv(filename):
    urls = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            url = row[2]
            urls.append(url)
    return urls

urls = read_links_from_csv('master_data.csv')

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

def get_master_price(url, filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[2] == url:
                return float(row[1])
    return None

def get_phone_number(url, filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[2] == url:
                return float(row[3])
    return None

price_drop_products = []
price_drop_list_url = []
price_drop_percentages = []
price_drop_numbers=[]

for url in urls:

    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_dom = et.HTML(str(soup))

    price = get_price(main_dom)
    product_name = get_name(main_dom)
    masterprice=get_master_price(url, 'master_data.csv')
    phonenumber=get_phone_number(url, 'master_data.csv')

    if price == masterprice:
        percentage = round((masterprice - price) * 100 / masterprice) #checking if what percentage of price changed
        if percentage >= 10:
            price_drop_products.append(product_name)
            price_drop_list_url.append(url)
            price_drop_percentages.append(percentage)
            price_drop_numbers.append(phonenumber)

if len(price_drop_products) == 0:
    print('No Price drop found')
else:
    for i in range(len(price_drop_products)):
        product_name = price_drop_products[i]
        percentage = price_drop_percentages[i]
        url = price_drop_list_url[i]
        phone_number = int(price_drop_numbers[i])

        text = f"Congrats! There is a {percentage}% drop in price for {product_name} Click here to purchase {url}"
        # Send text message using Twilio
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
                body = text,
                from_='+18447193470',
                to='+1'+str(phone_number)
            )
        print(f"Message sent to {phone_number} : {text}")