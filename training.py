from stock_price import *
from sentiment import *
import pandas as pd
import matplotlib.pyplot as plt

"""
PREREQUISITE 1: 
calling functions from sentiment analysis here to sentiment.json
e.g. sentiment_analysis("news.json")
"""

"""
PREREQUISITE 2:
calling functions from news scraping here to generate stock_price.json
"""

"""
analyse the relavance here
"""
def linear_plot():
    with open("stock_price.json", "r") as f:
        stock_data = json.load(f)
    
    with open("sentiment.json", "r") as f:
        sentiment_data = json.load(f)

    
    print(stock_data)
    print(sentiment_data)

if __name__ == "__main__":
    linear_plot()
