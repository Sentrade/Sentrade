#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__= "Nora&Yiwen"
__status__ = "Prototype"

import yfinance as yf  # pip install yfinance
import json


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
    stock = yf.Ticker("AAPL")  
    hist = stock.history(period=period)  

    # create the temp list dictionary
    temp = {}
    temp['date'] = []
    for date in hist.index:
        temp['date'].append(str(date)[:10])
    # print(temp['date'][1])
    for hist_key, hist_value in hist.items():
        temp[hist_key] = list(hist_value)
    # print(temp['open'][1])
    # DataFrame to json
    results = {}
    results['stock_name'] = stock_name

    results['items'] = [{'date': "", 'open': 0, 'high':0, 'low': 0, 'close':0, 'volume':0} for x in range(len(list(hist_value)))]
    # print(results['items'][0]['date'])
    for i in range(len(list(hist_value))):
        results['items'][i]['date'] = temp['date'][i]
        results['items'][i]['open'] = temp['open'][i]
        results['items'][i]['high'] = temp['high'][i]
        results['items'][i]['low'] = temp['low'][i]
        results['items'][i]['close'] = temp['close'][i]
        results['items'][i]['volume'] = temp['volume'][i]
    if not len(json_name):
        json_name = stock_name + '_' + period + '_' + 'stock_price_data.json'
    elif not json_name.endswith('.json'):
        json_name = json_name + '.json'

    with open(json_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(results, indent=4))
    return results


if __name__ == "__main__":
    import time
    import sys

    time1 = time.time()

    if len(sys.argv) >= 3:
        stock_name = sys.argv[1]
        period = sys.argv[2]
    else:
        stock_name = "AAPL"
        period = "1y"

    history_stock_price(stock_name=stock_name, period=period)
    print('history_stock_price costtime : {}'.format(round(time.time() - time1, 3)))
    # cost time heavily dependent on the network delay

