#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
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

company = "amazon"
with open("./{0}.json".format(company), 'r') as f:
	try:
		sentiment_data = [json.loads(line) for line in f]
	except:
		print("problem in reading ./{0}.json".format(company))
		exit(0)

stock_one_day = []
for record in sentiment_data:
	stock_one_day.append(float(record["1_day_sentiment_score"]["$numberDouble"]))
stock_one_day = np.array(stock_one_day)



