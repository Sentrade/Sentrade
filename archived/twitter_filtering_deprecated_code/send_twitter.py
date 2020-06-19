#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sent the twitter to the database.
"""

import pprint
from pymongo import MongoClient
import json

__author__ = "Ziyou Zhang"
__status__ = "Prototype"

def send_twitter(filename):

    # Setup the connection.
    client = MongoClient(os.environ["CLIENT_ADDR"])

    # Use the database sentrade_db.
    db = client.sentrade_db

    # Select the table to use.
    stock_db = db.news

    # insert from json file
    with open(filename, 'r', encoding='utf8', errors='ignore') as f:
        news_data = json.load(f)

    stock_db.insert_many(news_data)

    client.close()

if __name__ == "__main__":
    send_twitter("tw_all_companies.json")