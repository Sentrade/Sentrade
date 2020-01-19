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
    :return: json file including 'Date', 'Open','High','Low','Close','Volume'
    """
    stock = yf.Ticker("AAPL")  
    hist = stock.history(period=period)  

    # create the temp list dictionary
    temp = {}
    temp['Date'] = []
    for Date in hist.index:
        temp['Date'].append(str(Date)[:10])
    # print(temp['Date'][1])
    for hist_key, hist_value in hist.items():
        temp[hist_key] = list(hist_value)
    # print(temp['Open'][1])
    # DataFrame to json
    results = {}
    results['StockName'] = stock_name

    results['Items'] = [{'Date': "", 'Open': 0, 'High':0, 'Low': 0, 'Close':0, 'Volume':0} for x in range(len(list(hist_value)))]
    # print(results['Items'][0]['Date'])
    for i in range(len(list(hist_value))):
        results['Items'][i]['Date'] = temp['Date'][i]
        results['Items'][i]['Open'] = temp['Open'][i]
        results['Items'][i]['High'] = temp['High'][i]
        results['Items'][i]['Low'] = temp['Low'][i]
        results['Items'][i]['Close'] = temp['Close'][i]
        results['Items'][i]['Volume'] = temp['Volume'][i]
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

