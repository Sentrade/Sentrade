#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
from pymongo import MongoClient
import json

__author__ = "Yiwen Sun"
__status__ = "Development"

# Setup the connection.
client = MongoClient('mongodb://admin:sentrade@45.76.133.175:27017')

# Use the database sentrade_db. Select the table to use.
stock_db = client.sentrade_db.stock_price
sentiment_db = client.sentrade_data
# get all data
all_stock = stock_db.find({'company_name': 'GOOG'})
all_sentiment = sentiment_db.find({"company":"google"})

date = []
open = []
close = []
sentiment = []

for stock in all_stock:
    date.append(stock["date"])
    open.append(stock["open"])
    close.append(stock["close"])
change = [open_i - close_i for open_i, close_i in zip(open, close)]
print(change)

for entry in all_sentiment:
    sentiment.append(entry["1_day_sentiment_score"])
print(sentiment)

# delete data
# stock_db.drop()

client.close()
