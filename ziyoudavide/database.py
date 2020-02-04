#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient

__author__ = "Ziyou Zhang"
__status__ = "Prototype"

client = MongoClient()
db = client.test_database
db = client.sentrade_db

collection = db.stock_price

stock = {
            "date": "2020-01-21",
            "open": 317.19,
            "high": 319.02,
            "low": 316.02,
            "close": 316.57,
            "volume": 22240730
        }

db.stock_price.insert_one(stock)