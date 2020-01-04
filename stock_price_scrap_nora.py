# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 09:25:52 2019

@author: Nora
"""
import yfinance as yf   #pip install yfinance
import json


def show_cominfo(aapl):
    cominfo=aapl.info #取得公司信息
    print('AAPL cominfo:')
    for key,value in cominfo.items():
        print('{} : {}'.format(key,value))
    print()
    
def history_stock_price(stock_name="AAPL",period="2d",json_name=""):
    stock = yf.Ticker("AAPL")   ##soybean=yf.Ticker("SX19.CBT")   #期货
    hist = stock.history(period=period)   #取最长时间的历史价格数据    #1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    
    #DataFrame to json
    results = {}
    results['StockName'] = stock_name
    
    results['Date'] = []
    for Date in hist.index:
        results['Date'].append(str(Date))
    
    
    for hist_key,hist_value in hist.items():
        results[hist_key] = list(hist_value)
    
    if not len(json_name):
        json_name = stock_name + '_' + period + '_' +'stock_price_data.json'
    elif not json_name.endswith('.json'):
        json_name = json_name + '.json'
    
    with open(json_name,'w',encoding='utf-8') as f:
        f.write(json.dumps(results,indent=4))
    
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
        period="1y"
    
    history_stock_price(stock_name=stock_name,period=period)
    print('history_stock_price costtime : {}'.format(round(time.time() - time1,3)))
    # cost time heavily dependent on the network delay
    





    
    





