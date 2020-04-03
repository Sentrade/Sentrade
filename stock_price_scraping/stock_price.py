#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__= "Longzhen Li, Yiwen Sun"
__status__ = "Production"

import yfinance as yf
import json
from pymongo import MongoClient
# import pandas as pd

# def is_business_day(date):
#     return bool(len(pd.bdate_range(date, date)))

def history_stock_price(stock_name):
    """
	get historical stock price 

    :param stock_name:stock ticker
    :return: json file including 'date', 'open','high','low','close','volume'
    """
    stock = yf.Ticker(stock_name)  
    hist = stock.history(start="2018-11-01")  
    
    # create the temp list dictionary
    temp = {}
    temp['Date'] = []
    for date in hist.index:
        temp['Date'].append(str(date)[:10])
    for hist_key, hist_value in hist.items():
        temp[hist_key] = list(hist_value)
    results = {}
    print (hist_value)
    stock_count = len(list(hist_value))
    results = [{'date': "", 'company_name':"", 'open': 0, 'high':0, 'low': 0, 'close':0, 'volume':0, 'change': 0, 'rise': 0} for x in range(stock_count)]
    for i in range(stock_count):
        results[i]['company_name'] = stock_name
        results[i]['open'] = temp['Open'][i]
        results[i]['date'] = temp['Date'][i]
        results[i]['high'] = temp['High'][i]
        results[i]['low'] = temp['Low'][i]
        results[i]['close'] = temp['Close'][i]
        results[i]['volume'] = temp['Volume'][i]
    
    for i in range(1, stock_count):
        results[i]['change'] = results[i]['close'] - results[i-1]['close']
        results[i]['rise'] = 1 if results[i]['change'] > 0 else 0

    return results

if __name__ == "__main__":
    from pymongo import MongoClient
    import json

    client = MongoClient('mongodb://admin:sentrade@45.76.133.175:27017')
    stock_list = ['AAPL', 'TSLA', 'AMZN', 'FB', 'GOOG', 'MSFT', 'NFLX', 'UBER']

    db = client.sentrade_db
    stock_db = db.stock_price
    stock_db.drop()

    for stocks in stock_list: 
        stock_output = history_stock_price(stock_name=stocks)
        stock_db.insert_many(stock_output)    

    client.close()