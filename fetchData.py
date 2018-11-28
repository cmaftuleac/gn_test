#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

import requests
from lxml import html
from pymongo import MongoClient

SOURCES = (
    {'url': 'https://www.investing.com/commodities/silver-historical-data', 'type': 'silver'},
    {'url': 'https://www.investing.com/commodities/gold-historical-data', 'type': 'gold'}
)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
client = MongoClient('localhost', 27017)
db = client.investing_com
collection = db.prices


def fetch_data(url, commodity_type):
    print('\nGetting historical {} prices from investing.com'.format(commodity_type))
    try:
        data = requests.get(url, headers=HEADERS)
        data.raise_for_status()
        tree = html.fromstring(data.content)

        dates = tree.xpath("//table[@id='curr_table']/tbody/tr/td[1]/@data-real-value")
        prices = tree.xpath("//table[@id='curr_table']/tbody/tr/td[2]/text()")

        formated_dates = [datetime.fromtimestamp(float(date)) for date in dates]

        for date, price in zip(formated_dates, prices):
            collection.insert_one({'date': date, 'price': float(price.replace(',', '')), 'type': commodity_type})

        print('Historical {} prices collected with success.'.format(commodity_type))
    except requests.exceptions.RequestException as e:
        print('Oops, something went wrong! {}'.format(e))


def main():
    print('Fetching starts!')
    for source in SOURCES:
        fetch_data(source.get('url'), source.get('type'))


if __name__ == '__main__':
    main()
