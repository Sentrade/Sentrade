#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
from pymongo import MongoClient
import matplotlib.pyplot as plt

__author__ = "Yiwen Sun, Ziyou Zhang ;)"
__status__ = "Development"

def data_study(ticker_name):

    company_db_name = {
    "AMZN"  : "amazon",
    "AAPL"  : "apple", 
    "FB"    : "facebook",
    "GOOG"  : "google",
    "MSFT"  : "microsoft",
    "NFLX"  : "netflix",
    "TSLA"  : "tesla",
    "UBER"  : "uber"
    }

    # Setup the connection.
    client = MongoClient('mongodb://admin:sentrade@45.76.133.175:27017')

    # Use the database sentrade_db. Select the table to use.
    stock_db = client.sentrade_db.stock_price
    sentiment_db = client.sentiment_data[company_db_name[ticker_name]]
    # get all data
    all_stock = stock_db.find({'company_name': ticker_name}).sort("date")
    all_sentiment = sentiment_db.find().sort("date")

    date = []
    open = []
    close = []
    change = []
    sentiment_date = []
    sentiment = []

    for stock in all_stock:
        date.append(stock["date"])
        open.append(stock["open"])
        close.append(stock["close"])
    
    for i in range(len(date)-1):
        change.append(open[i+1] - close[i])

    for entry in all_sentiment:
        sentiment_date.append(entry["date"])
        sentiment.append(entry["1_day_sentiment_score"])

    client.close()

    change_plot = []
    sentiment_plot = []
    for i in range(len(date)):
        for j in range(len(sentiment_date)):
            if date[i] == sentiment_date[j]:
                change_plot.append(change[i])
                sentiment_plot.append(sentiment[j])

    plt.plot(sentiment_plot, change_plot, '.')
    plt.show()

def get_previous_date(current_date):
    previous_date = ""
    return previous_date

if __name__ == "__main__":
    tickers = ["AMZN", "AAPL", "FB", "GOOG", "MSFT", "NFLX", "TSLA", "UBER"]
    for ticker in tickers:
        data_study(ticker)