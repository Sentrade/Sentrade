#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The helper script to modify twitter time in the database.
"""

from pymongo import MongoClient
import json

__author__ = "Ziyou Zhang"
__status__ = "Prototype"

day = {
    "Mon": "01",
    "Tue": "02",
    "Wed": "03",
    "Thu": "04",
    "Fri": "05",
    "Sat": "06",
    "Sun": "07" 
}

month = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}

def get_twitter_date():

    client = MongoClient('mongodb://admin:sentrade@45.76.133.175:27017')
    db = client.sentrade_db
    news_db = db.news
    all_news = news_db.find()

    for news in all_news:
        if news["created_at"]:
            time_string = news["created_at"]
            words = time_string.split(" ")
            date = words[-1] + "-" + month[words[1]] + "-" + words[2]
            updated_date = {"$set": {"date": date}}
            news_db.update_one(news, updated_date)

    client.close()


if __name__ == "__main__":
    get_twitter_date()