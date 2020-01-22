#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from blobsentiment import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

__author__ = "Ziyou Zhang"
__status__ = "Prototype"

def correlation_analysis(news_file, sentiment_file, stock_file):
    """
    Initial plot about the stock price and sentiment for figuring out the pattern.

    :param news_file: the news file to run sentiment analysis on.
    :param sentiment_file: the file containing the sentiment information.
    :param stock_file: the file containing the stock price data.
    """
    raw_blob_analysis(news_file, sentiment_file)

    with open(sentiment_file, "r") as f:
        sentiment_data = json.load(f)

    with open(stock_file, "r") as f:
        stock_data = json.load(f)
    
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
    
    # print(news_dates)
    # print(news_scores)
    # print("sentiment data ready")

    dates = []
    price_changes = []
    sentiment_scores = []
    
    for stock_entry in stock_data["items"]:
        date = stock_entry["date"]
        open_price = stock_entry["open"]
        close_price = stock_entry["close"]
        for i in range(len(news_dates)):
            if (news_dates[i] == date):
                dates.append(date)
                price_changes.append(close_price - open_price)
                sentiment_scores.append(news_scores[i])

    return sentiment_scores, price_changes

def volumn_study():
    """
    Plot the hisorical apple stock price change data and volume to study the correlation.
    """
    with open("AAPL_max_stock_price_data.json", "r") as f:
        stock_data = json.load(f)
    date = stock_data['items']["date"]
    open_price = stock_data['items']["open"]
    close_price = stock_data['items']["close"]
    volume = stock_data['items']["volume"]

    print(len(open_price))

    stock_price_change = []
    for i in range(len(open_price)):
        stock_price_change.append(open_price[i] - close_price[i])

    plt.plot(stock_price_change, volume, '.')
    plt.show()
    
                
if __name__ == "__main__":
    correlation_analysis("temp_twitter.json", "temp_sentiment.json", "temp_stock.json")
