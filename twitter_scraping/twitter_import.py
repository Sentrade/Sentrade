#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Twitter scrapying code.
"""

from pymongo import MongoClient
import json

__author__ = "Ziyou Zhang"
__status__ = "Prototype"

client = MongoClient('mongodb://admin:sentrade@45.76.133.175:27017')

db = client.twitter_current

with open("./results/uber-2020-04-06.json") as f:
    twitter_data = json.load(f)

db["uber"].insert_many(twitter_data)

client.close()