#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Process the data in the news and put in the sentiment database.
"""

from pymongo import MongoClient
import json

__author__ = "Ziyou Zhang"
__status__ = "Development"

def process_sentiment():

    client = MongoClient('mongodb://admin:sentrade@45.76.133.175:27017')
    db = client.sentrade_db
    twitter_db = client.twitter_data

    apple_news_db = twitter_db.apple
    apple_news = apple_news_db.find()
    for apple_news_entry in apple_news:
        pass

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

if __name__ == "__main__":
    process_sentiment()
