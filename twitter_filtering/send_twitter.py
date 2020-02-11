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
    client = MongoClient('mongodb://admin:sentrade@45.76.133.175:27017')

    # Use the database sentrade_db.
    db = client.sentrade_db

    # Select the table to use.
    new_db = db.news

    # insert from json file
    with open(filename) as f:
        news_data = json.load(f)

    new_db.insert_many(news_data)

if __name__ == "__main__":
    send_twitter("temp_sentiment.json")