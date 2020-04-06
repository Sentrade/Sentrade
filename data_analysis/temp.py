#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import joblib
import pymongo

__author__ = "Fengming Liu"
__status__ = "Development"

db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
company = "amazon"
db_collection = db_client["sentiment_data"][company]
senti_df = pd.DataFrame()
for record in db_collection.find():
	senti_df = senti_df.append(record, ignore_index=True)
print(senti_df)

senti_df.dropna(inplace=True)
senti_df.insert(loc=1, column="relative_day", value=None)
for index, row in senti_df.iterrows():
    senti_df.loc[index, "relative_day"] = get_relativeday(row["date"].date()) 
    senti_df.loc[index, "1_day_sentiment_score"] = float(row["1_day_sentiment_score"]["$numberDouble"])
    senti_df.loc[index, "1_day_news_count"] = int(row["1_day_news_count"]["$numberInt"])
    senti_df.loc[index, "1_day_overall_sentiment_score"] = float(row["1_day_overall_sentiment_score"]["$numberDouble"])
senti_df.drop(["_id", "date"], axis=1, inplace=True)

# # merge data
# total_df = pd.merge(senti_df, stock_df, on=["company", "relative_day"])
total_df.insert(loc=3, column="past_3_days_senti_avg", value=None)
total_df.insert(loc=3, column="past_7_days_senti_avg", value=None)
# total_df.insert(loc=1, column="up_rate", value=None)
# total_df.insert(loc=2, column="up_cat", value=None)

# for index, row in total_df.iterrows():
#     # calculate average sentimen scores
#     current_day = row["relative_day"]
#     past_days_scores = []
#     for i in range(1, 8):
#         past_record = total_df[total_df["relative_day"]==current_day - i]
#         if past_record.empty:
#             # if no value, then sentiment scores is 0 (neutral sentiment) by default
#             past_days_scores.append(float(0))
#         else:
#             past_days_scores.append(past_record["1_day_sentiment_score"].iloc[0])

#     total_df.loc[index, "past_3_days_senti_avg"] = (past_days_scores[0] + past_days_scores[1] + past_days_scores[2])/3
#     total_df.loc[index, "past_7_days_senti_avg"] = np.mean(past_days_scores)
    
#     # calculate percentage chanes of stock price
#     current_stock = row["close"]
#     last_stock = total_df[total_df["relative_day"] == current_day - 1]
#     if last_stock.empty:
#         total_df.loc[index, "up_rate"] = float(0)
#     else:
#         last_stock = last_stock["close"].iloc[0]
#         total_df.loc[index, "up_rate"] = (current_stock - last_stock) / last_stock
    
#     up_rate = total_df.loc[index, "up_rate"]
#     if up_rate >= 0.05:
#         total_df.loc[index, "up_cat"] = 2
#     elif up_rate < 0.05 and up_rate >= 0.01:
#         total_df.loc[index, "up_cat"] = 1
#     elif up_rate < 0.01 and up_rate > -0.01:
#         total_df.loc[index, "up_cat"] = 0
#     elif up_rate <= -0.01 and up_rate > -0.05:
#         total_df.loc[index, "up_cat"] = -1
#     else:
#         total_df.loc[index, "up_cat"] = -2