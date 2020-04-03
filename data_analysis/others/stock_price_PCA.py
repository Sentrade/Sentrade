#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from sklearn.decomposition import PCA
import numpy as np
import json

__author__ = "Yiwen Sun, Ziyou Zhang, Fengming Liu"
__status__ = "Development"

# companies = ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]
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

# get all data
# client = MongoClient("mongodb://admin:sentrade@45.76.133.175:27017")
# client = MongoClient("mongodb://admin:sentrade@127.0.0.1:27017")
# stock_db = client.sentrade_db.stock_price
# sentiment_db = client.sentiment_data[company]
# all_stock = stock_db.find({'company_name': company_to_ticker[company]}).sort("date")
# all_sentiment = sentiment_db.find().sort("date")

company = "amazon"
with open("./{0}.json".format(company), 'r') as f:
	try:
		sentiment_data = [json.loads(line) for line in f]
	except:
		print("problem in reading ./{0}.json".format(company))
		exit(0)

for record in sentiment_data:
	print(record["date"], float(record["1_day_sentiment_score"]["$numberDouble"]))

# stock_date = []
# stock_open = []
# stock_close = []
# stock_change = []
# sentiment_date = []
# sentiment_score = []
# sentiment_overall = []

# for stock in all_stock:
#     stock_date.append(stock["date"])
#     stock_open.append(stock["open"])
#     stock_close.append(stock["close"])

# print(stock_open)

# # stock price difference between tomorrow's open and today's close
# for i in range(len(stock_date)-1):
#     stock_change.append(stock_open[i+1] - stock_close[i])

# for sentiment in all_sentiment:
#     sentiment_date.append(sentiment["date"])
#     sentiment_score.append(sentiment["1_day_sentiment_score"])
#     # sentiment_overall.append(sentiment["1_day_overall_sentiment_score"])

# client.close()