#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Twitter scrapying code.
"""

__author__ = "Ziyou Zhang"
__status__ = "Production"

from pymongo import MongoClient
import json


client = MongoClient(os.environ["CLIENT_ADDR"])

db = client.twitter_current

with open("./results/uber-2020-04-06.json") as f:
    twitter_data = json.load(f)

db["uber"].insert_many(twitter_data)

client.close()