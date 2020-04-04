#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import datetime
import pandas as pd

__author__ = "Fengming Liu"
__status__ = "Development"

def format_date(date):
	result = datetime.datetime.strptime(date, "%Y-%m-%d")
	return result.date()

def get_relativeday(date):
    rel_days = (date - datetime.date(2019, 1, 1)).days
#    print(type(rel_days))
    return rel_days

def get_weekday(date):
	[year, month, day] = date.split('-')
	return datetime.date(int(year), int(month), int(day)).weekday() + 1

def get_num(num_dict):
	if "$numberInt" in num_dict:
		return float(num_dict["$numberInt"])
	elif "$numberDouble" in num_dict:
		return float(num_dict["$numberDouble"])
	else:
		return 0

##### main #####
company_list = ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]
ticker_to_company = {
    "AMZN"		: "amazon",
    "AAPL"		: "apple",
    "FB"		: "facebook",
    "GOOG"		: "google",
    "MSFT"		: "microsoft",
    "NFLX"		: "netflix",
    "TSLA"		: "tesla",
    "UBER"		: "uber"
}

# preprocess stock data
stock_df = pd.read_json("./stock_price.json", lines=True)
stock_df.insert(loc=0, column="relative_day", value=None)
stock_df.rename(columns={"company_name": "company"}, inplace=True)
for index, row in stock_df.iterrows():
    stock_df.loc[index, "relative_day"] = get_relativeday(row["date"].date())
    stock_df.loc[index, "company"] = ticker_to_company[row["company"]]
    stock_df.loc[index, "open"] = get_num(row["open"])
    stock_df.loc[index, "high"] = get_num(row["high"])
    stock_df.loc[index, "low"] = get_num(row["low"])
    stock_df.loc[index, "close"] = get_num(row["close"])
    stock_df.loc[index, "volume"] = get_num(row["volume"])    
    
stock_df.drop(["_id", "date"], axis=1, inplace=True)

for company in company_list:
    # preprocess sentiment data
    senti_df = pd.read_json("./sentiment_score/{0}.json".format(company), lines=True)
    senti_df.dropna(inplace=True)
    senti_df.insert(loc=1, column="relative_day", value=None)
    for index, row in senti_df.iterrows():
        senti_df.loc[index, "relative_day"] = get_relativeday(row["date"].date()) 
        senti_df.loc[index, "1_day_sentiment_score"] = float(row["1_day_sentiment_score"]["$numberDouble"])
        senti_df.loc[index, "1_day_news_count"] = int(row["1_day_news_count"]["$numberInt"])
        senti_df.loc[index, "1_day_overall_sentiment_score"] = float(row["1_day_overall_sentiment_score"]["$numberDouble"])
    senti_df.drop(["_id", "date"], axis=1, inplace=True)

    # merge data
    total_df = pd.merge(senti_df, stock_df, on=["company", "relative_day"])
    total_df.insert(loc=3, column="past_3_days_senti_avg", value=None)
    total_df.insert(loc=3, column="past_7_days_senti_avg", value=None)
    total_df.insert(loc=1, column="up_rate", value=None)
    total_df.insert(loc=2, column="up_cat", value=None)
    
    for index, row in total_df.iterrows():
        # calculate average sentimen scores
        current_day = row["relative_day"]
        past_days_scores = []
        for i in range(1, 8):
            past_record = total_df[total_df["relative_day"]==current_day - i]
            if past_record.empty:
                # if no value, then sentiment scores is 0 (neutral sentiment) by default
                past_days_scores.append(float(0))
            else:
                past_days_scores.append(past_record["1_day_sentiment_score"].iloc[0])
    
        total_df.loc[index, "past_3_days_senti_avg"] = (past_days_scores[0] + past_days_scores[1] + past_days_scores[2])/3
        total_df.loc[index, "past_7_days_senti_avg"] = np.mean(past_days_scores)
        
        # calculate percentage chanes of stock price
        current_stock = row["close"]
        last_stock = total_df[total_df["relative_day"] == current_day - 1]
        if last_stock.empty:
            total_df.loc[index, "up_rate"] = float(0)
        else:
            last_stock = last_stock["close"].iloc[0]
            total_df.loc[index, "up_rate"] = (current_stock - last_stock) / last_stock
        
        up_rate = total_df.loc[index, "up_rate"]
        if up_rate >= 0.05:
            total_df.loc[index, "up_cat"] = 2
        elif up_rate < 0.05 and up_rate >= 0.01:
            total_df.loc[index, "up_cat"] = 1
        elif up_rate < 0.01 and up_rate > -0.01:
            total_df.loc[index, "up_cat"] = 0
        elif up_rate <= -0.01 and up_rate > -0.05:
            total_df.loc[index, "up_cat"] = -1
        else:
            total_df.loc[index, "up_cat"] = -2
        
    total_df.to_csv("./processed_data/{0}_clf.csv".format(company))
    
















