#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__= "Nora&Yiwen"
__status__ = "Development"

import yfinance as yf
import json
from pymongo import MongoClient

def show_cominfo(aapl):
    """
    acquire company information
    
    :param aapl:stock ticker
    """
    cominfo = aapl.info  
    print('AAPL cominfo:')
    for key, value in cominfo.items():
        print('{} : {}'.format(key, value))
    print()


def history_stock_price(stock_name="AAPL", period="2d", json_name=""):
    """
	get historical stock price 

    :param stock_name:stock ticker
    :param period:time period from 1d to max (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)
    :param json_name: name of the output file
    :return: json file including 'date', 'open','high','low','close','volume'
    """
    stock = yf.Ticker(stock_name)  
    hist = stock.history(period=period)  
    
    # create the temp list dictionary
    temp = {}
    temp['Date'] = []
    for date in hist.index:
        temp['Date'].append(str(date)[:10])
    # print(temp['Date'][1])
    for hist_key, hist_value in hist.items():
        temp[hist_key] = list(hist_value)
    # print(temp['Open'][1])
    # DataFrame to json
    results = {}
    print (hist_value)
    results = [{'date': "", 'company_name':"", 'open': 0, 'high':0, 'low': 0, 'close':0, 'volume':0} for x in range(len(list(hist_value)))]
    for i in range(len(list(hist_value))):
        results[i]['company_name'] = stock_name
        results[i]['open'] = temp['Open'][i]
        results[i]['date'] = temp['Date'][i]
        results[i]['high'] = temp['High'][i]
        results[i]['low'] = temp['Low'][i]
        results[i]['close'] = temp['Close'][i]
        results[i]['volume'] = temp['Volume'][i]

    json_name += stock_name + '_' + period + '_' + 'stock_price_data.json'

    with open(json_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(results, indent=4))

    return results

if __name__ == "__main__":
    import time
    import sys
    from pymongo import MongoClient
    import json

    # Setup the connection.
    client = MongoClient('mongodb://admin:sentrade@45.76.133.175:27017')

    # Use the database sentrade_db.
    db = client.sentrade_db

    # Select the table to use.
    stock_db = db.stock_price

    time1 = time.time()

    if len(sys.argv) >= 3:
        stock_name = sys.argv[1]
        period = sys.argv[2]
    else:
        period = "max"

    stock_list = ['AAPL', 'TSLA', 'AMZN','FB', 'GOOG', 'MSFT', 'NFLX', 'UBER']
    for stocks in stock_list: 
        stock_output = history_stock_price(stock_name=stocks, period=period)
        stock_db.insert_many(stock_output)    
    print('history_stock_price costtime : {}'.format(round(time.time() - time1, 3)))
    # cost time heavily dependent on the network delay
