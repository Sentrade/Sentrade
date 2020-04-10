#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
from pymongo import MongoClient
import matplotlib.pyplot as plt
from pathlib import Path

__author__ = "Yiwen Sun, Ziyou Zhang ;)"
__status__ = "Development"

def data_study(company_name, client_address):

    company_to_ticker = {
        "amazon"    : "AMZN",
        "apple"     : "AAPL", 
        "facebook"  : "FB",
        "google"    : "GOOG",
        "microsoft" : "MSFT",
        "netflix"   : "NFLX",
        "tesla"     : "TSLA",
        "uber"      : "UBER"
    }

    # Setup the connection.
    client = MongoClient(client_address)

    # Use the database sentrade_db. Select the table to use.
    stock_db = client.sentrade_db.stock_price
    sentiment_db = client.sentiment_data[company_name]
    # get all data
    all_stock = stock_db.find({'company_name': company_to_ticker[company_name]}).sort("date")
    all_sentiment = sentiment_db.find().sort("date")

    stock_date = []
    stock_open = []
    stock_close = []
    stock_change = []
    sentiment_date = []
    sentiment_score = []
    sentiment_overall = []

    for stock in all_stock:
        stock_date.append(stock["date"])
        stock_open.append(stock["open"])
        stock_close.append(stock["close"])
    
    # stock price difference between tomorrow's close and today's close
    for i in range(len(stock_date)-1):
        stock_change.append((stock_close[i+1] - stock_close[i])/stock_close[i] * 100)

    for sentiment in all_sentiment:
        sentiment_date.append(sentiment["date"])
        sentiment_score.append(sentiment["1_day_sentiment_score"])
        # sentiment_overall.append(sentiment["1_day_overall_sentiment_score"])

    client.close()

    change_plot = []
    sentiment_plot = []
    sentiment_overall_plot = []
    for i in range(len(stock_date)):
        for j in range(len(sentiment_date)):
            if stock_date[i] == sentiment_date[j]:
                change_plot.append(stock_change[i])
                sentiment_plot.append(sentiment_score[j])
                # sentiment_overall_plot.append(sentiment_overall[j])

    plt.plot(sentiment_plot, change_plot, 'k.')
    plt.title(company_name)
    plt.xlabel("1 day average sentiment score")
    plt.ylabel("stock price change percentage / %")
    plt.savefig(Path("./scatter/" + company_name + "_average.png"))
    plt.clf()

    # plt.plot(sentiment_plot, change_plot, 'b.')
    # plt.title(company_name)
    # plt.xlabel("1 day average overall sentiment score")
    # plt.ylabel("stock price change")
    # plt.savefig(Path("/scatter/" + company_name + "_overall.png"))

    print("Plot for", company_name, "finished")

if __name__ == "__main__":
    client_address = "mongodb://admin:sentrade@45.76.133.175:27017"
    companies = ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]
    for company in companies:
        data_study(company, client_address)