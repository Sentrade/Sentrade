#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Process the data in the news and put in the sentiment database.
"""

from pymongo import MongoClient
import json

__author__ = "Ziyou Zhang"
__status__ = "Prototype"

def process_sentiment():

    client = MongoClient('mongodb://admin:sentrade@45.76.133.175:27017')
    db = client.sentrade_db
    stock_db = db.stock_price
    stock_list = ['AAPL', 'TSLA', 'AMZN','FB', 'GOOG', 'MSFT', 'NFLX', 'UBER']

    news_dates = []
    news_scores = []
    today_news_count = 0
    today_news_score = 0

    # print("json objects prepared")

    for sentiment_entry in sentiment_data:
        if sentiment_entry["date"] not in news_dates:
            news_dates.append(sentiment_entry["date"])
            if today_news_count != 0:
                news_scores.append(today_news_score / today_news_count)
            today_news_score = 0
            today_news_count = 0
        today_news_count += 1
        today_news_score += sentiment_entry["polarity"]
    
    if today_news_count != 0:
        news_scores.append(today_news_score / today_news_count)
