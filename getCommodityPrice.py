#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from statistics import variance, mean

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.investing_com
collection = db.prices


def get_commodity_price(start_date, end_date, commodity_type):
    s_date = datetime.strptime(start_date, '%Y-%m-%d')
    e_date = datetime.strptime(end_date, '%Y-%m-%d')
    prices = [x['price'] for x in collection.find({'date': {'$gt': s_date, '$lt': e_date, }, 'type': commodity_type})]
    prices_mean = mean(prices)
    prices_variance = variance(prices, prices_mean)
    print(commodity_type, prices_mean, prices_variance)


def main():
    get_commodity_price(sys.argv[1], sys.argv[2], sys.argv[3])
    collection.drop()


if __name__ == '__main__':
    main()
