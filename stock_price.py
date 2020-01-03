"""
The python package for scrapying the stock price data.
"""
import yfinance as yf
import pandas as pd

def scrap_stock(index,start,end):
    aapl = yf.download(index,start,end,group_by="ticker")
    closeappl = aapl['Close']
    print (closeappl)

if __name__ == "__main__":
    scrap_stock('TSLA','2019-12-01','2019-12-30')
