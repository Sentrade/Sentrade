#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import joblib
import datetime
import pymongo
import time


__author__ = "Fengming Liu"
__status__ = "Development"

def get_relativeday(date):
    [year, month, day] = date.split('-')
    rel_days = (datetime.date(int(year), int(month), int(day)) - datetime.date(2019, 1, 1)).days
    return rel_days

def get_company_code(record, company):
    for name in ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla"]:
        record["company_"+name] = 0
    record["company_" + company] = 1
    return record
    
def preprocess_data(record, company, date):
    # calculate the features
    record["relative_day"] = get_relativeday(record["date"])
    record = get_company_code(record, company)
    record["1_day_sentiment_score"] = float(record["1_day_sentiment_score"])
    record["1_day_news_count"] = int(record["1_day_news_count"])
    record["1_day_overall_sentiment_score"] = float(record["1_day_overall_sentiment_score"])
    keys = record.keys()
    if "past_3_days_senti_avg" in keys:
        record["past_3_days_senti_avg"] = float(record["past_3_days_senti_avg"])
    else:
        record["past_3_days_senti_avg"] = float(0)
    if "past_7_days_senti_avg" in keys:
        record["past_7_days_senti_avg"] = float(record["past_7_days_senti_avg"])
    else:
        record["past_7_days_senti_avg"] = float(0)

    # return the necessary features
    result = []
    for key, value in record.items():
        if key in [
#                   "relative_day", 
                   "1_day_sentiment_score", 
                   "1_day_news_count",
#                   "1_day_overall_sentiment_score", 
                   "past_3_days_senti_avg",
                   "past_7_days_senti_avg", 
                   "company_amazon", 
                   "company_apple",
                   "company_facebook", 
                   "company_google", 
                   "company_microsoft",
                   "company_netflix", 
                   "company_tesla"
                   ]:
            result.append(value)
    
    return np.array(result).reshape(1, -1)
            
def on_click(clf, x_test):
    y_pred = clf.predict(x_test) # a np.array
    return y_pred

if __name__ == "__main__":
    time_log = open("./UI_time.log", 'a')
    
    # load the pretrained model
    clf = joblib.load("./models/SVM_model.joblib")
    
    # connect to the database
    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
    db = db_client["sentiment_current"]
    
    # get the sentiment data for the company
#    company = get_company() # get the comapny name from the UI
#    date = get_date() # get the date from the UI
#                      # date must be of the format yyyy-mm-dd
    company = "amazon"
    date = "2020-04-06"
    
    # fetch the data from the database
    start_tick = time.time()
    db_collection = db[company]
    record = db_collection.find_one({"date": date})
    end_tick = time.time()
    time_log.write("{0:15s}	{1:20s} {2:.3f}\n".format(date, "Data fetching", end_tick - start_tick))
    
    # preprocess the data
    start_tick = time.time()
    x_test = preprocess_data(record, company, date) 
    end_tick = time.time()
    time_log.write("{0:15s}	{1:20s} {2:.3f}\n".format(date, "Data preprocessing", end_tick - start_tick))
    
    # do the prediction
    start_tick = time.time()
    result = on_click(clf, x_test)
    end_tick = time.time()
    time_log.write("{0:15s}	{1:20s} {2:.3f}\n".format(date, "Prediction", end_tick - start_tick))
    
    print(result[0])
    time_log.close()