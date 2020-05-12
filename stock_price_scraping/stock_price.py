#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__= "Longzhen Li, Yiwen Sun"
__status__ = "Production"

import yfinance as yf
import json
import os
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
    # print(stock.info)
    
    # create the temp list dictionary
    temp = {}
    temp['Date'] = []
    for date in hist.index:
        temp['Date'].append(str(date)[:10])
    for hist_key, hist_value in hist.items():
        temp[hist_key] = list(hist_value)
    results = {}
    stock_count = len(list(hist_value))
    results = [{'date': "", 'company_name':"", 'open': 0, 'high':0, 'low': 0, 'close':0, 'volume':0, 'change': 0, 'rise': 0, 'change rate': 0, 'label': 0} for x in range(stock_count)]
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
    
    print("current ticker:", stock_name)

    return results

def stock_price_database(company_name, client_address):
    """
	get historical stock price and put in the stock database.

    :param company_name: name of the company
    :param client_address: the database address
    """

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

    stock_name = company_to_ticker[company_name]

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

    stock_count = len(list(hist_value))
    results = [{'date': "", 'company_name':"", 'open': 0, 'high':0, 'low': 0, 'close':0, 'volume':0, 'change': 0, 'rise': 0, 'change rate': 0, 'label': 0} for x in range(stock_count)]
    for i in range(stock_count):
        results[i]['company_name'] = company_name
        results[i]['open'] = temp['Open'][i]
        results[i]['date'] = temp['Date'][i]
        results[i]['high'] = temp['High'][i]
        results[i]['low'] = temp['Low'][i]
        results[i]['close'] = temp['Close'][i]
        results[i]['volume'] = temp['Volume'][i]
    
    for i in range(1, stock_count):
        results[i]['change'] = results[i]['close'] - results[i-1]['close']
        results[i]['rise'] = 1 if results[i]['change'] > 0 else 0
        results[i]['change rate'] = results[i]['change'] / results[i]['close']
        if results[i]['change rate'] >= 0.05:
            results[i]['label'] = 2
        if results[i]['change rate'] < 0.05 and results[i]['change rate'] >= 0.01:
            results[i]['label'] = 1
        if results[i]['change rate'] < 0.01 and results[i]['change rate'] > -0.01:
            results[i]['label'] = 0
        if results[i]['change rate'] <= -0.01 and results[i]['change rate'] > -0.05:
            results[i]['label'] = -1
        if results[i]['change rate'] <= -0.05:
            results[i]['label'] = -2

    client = MongoClient(client_address)
    db = client.stock_data
    stock_db = db[company_name]
    stock_db.drop()
    stock_db.insert_many(results)
    client.close()

    print("current company:", company_name)

if __name__ == "__main__":

    # client = MongoClient('mongodb://admin:sentrade@45.76.133.175:27017')
    # stock_list = ['AAPL', 'TSLA', 'AMZN', 'FB', 'GOOG', 'MSFT', 'NFLX', 'UBER']

    # db = client.sentrade_db
    # stock_db = db.stock_price
    # stock_db.drop()

    # for stocks in stock_list: 
    #     stock_output = history_stock_price(stock_name=stocks)
    #     stock_db.insert_many(stock_output)    

    # client.close()

    client_address = 'mongodb://admin:sentrade@45.76.133.175:27017'
    companies = ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]
    for company in companies:
        stock_price_database(company, client_address)