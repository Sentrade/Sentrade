#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from bson import json_util
import json

__author__ = "Ziyou Zhang"
__status__ = "Prototype"

client = MongoClient()
db = client.test_database
db = client.sentrade_db

with open('temp_stock.json') as f:
    stock_data = json.load(f)
    db.stock_price.insert_many(stock_data)

client.close()
