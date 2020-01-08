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

    dates = []
    price_changes = []
    sentiment_scores = []
    
    for stock_entry in stock_data:
        date = stock_entry["date"]
        open_price = stock_entry["open"]
        close_price = stock_entry["close"]
        for sentiment_entry in sentiment_data:
            if (sentiment_entry["date"] == date):
                dates.append(date)
                price_changes.append(close_price-open_price)
                sentiment_scores.append(sentiment_entry["polarity"])

    print (dates)
    print (price_changes)
    print (sentiment_scores)

    plt.plot(sentiment_scores, price_changes, '.')
    plt.show()
                
if __name__ == "__main__":
    linear_plot()
