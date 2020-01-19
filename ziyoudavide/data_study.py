#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from stock_price import *
from blobsentiment import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

__author__ = "Ziyou Zhang"
__status__ = "Prototype"

def scatter_plot(news_file, sentiment_file, stock_file):
    """
    Initial plot about the stock price and sentiment for figuring out the pattern.

    :param news_file: the news file to run sentiment analysis on.
    :param sentiment_file: the file containing the sentiment information.
    :param stock_file: the file containing the stock price data.
    """
    blob_analyse(news_file, sentiment_file)

    with open(sentiment_file, "r") as f:
        sentiment_data = json.load(f)

    with open(stock_file, "r") as f:
        stock_data = json.load(f)
    
    dates = []
    price_changes = []
    sentiment_scores = []
    
    for stock_entry in stock_data:
        date = stock_entry["date"]
        open_price = stock_entry["open"]
        close_price = stock_entry["close"]
        for sentiment_entry in sentiment_data:
            if (sentiment_entry["date"] == date):
                dates.append(date)
                price_changes.append(close_price-open_price)
                sentiment_scores.append(sentiment_entry["polarity"])

    print (dates)
    print (price_changes)
    print (sentiment_scores)

    plt.plot(sentiment_scores, price_changes, '.')
    plt.show()

def volumn_study():
    """
    Plot the hisorical apple stock price change data and volume to study the correlation.
    """
    with open("AAPL_max_stock_price_data.json", "r") as f:
        stock_data = json.load(f)
    date = stock_data["Date"]
    open_price = stock_data["Open"]
    close_price = stock_data["Close"]
    volume = stock_data["Volume"]

    print(len(open_price))

    stock_price_change = []
    for i in range(len(open_price)):
        stock_price_change.append(open_price[i] - close_price[i])

    plt.plot(stock_price_change, volume, '.')
    plt.show()
    
                
if __name__ == "__main__":
    scatter_plot("temp.json", "sentiment.json", "stock_price.json")
