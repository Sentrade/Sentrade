#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sample database operations.

The documents can be found here:
https://api.mongodb.com/python/current/tutorial.html
http://zetcode.com/python/pymongo/
"""

import pprint
from pymongo import MongoClient
import json

__author__ = "Ziyou Zhang"
__status__ = "Prototype"

# Setup the connection.
client = MongoClient('mongodb://admin:sentrade@45.76.133.175:27017')

# Use the database sentrade_db.
db = client.sentrade_db

# Select the table to use.
stock_db = db.stock_price

# Prepare the data.
stock = {
            "date": "2020-01-21",
            "open": 317.19,
            "high": 319.02,
            "low": 316.02,
            "close": 316.57,
            "volume": 22240730
        }

# Insert the data into the database.
stock_db.insert_one(stock)

# Get one data set that satisfies the condition and print it.
one_stock = stock_db.find_one({"date": "2020-01-21"})
pprint.pprint(one_stock)

# Count elements.
print(stock_db.count_documents({}))

# insert from json file
with open("temp_stock.json") as f:
    stock_data = json.load(f)

stock_db.insert_many(stock_data)

# get all data
all_stock = stock_db.find()
# for stock in all_stock:
#     print(stock)

# delete data
# stock_db.drop()

client.close()
