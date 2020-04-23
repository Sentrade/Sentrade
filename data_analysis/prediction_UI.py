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

def get_num(num_dict):
	if "$numberInt" in num_dict:
		return float(num_dict["$numberInt"])
	elif "$numberDouble" in num_dict:
		return float(num_dict["$numberDouble"])
	else:
		return 0
    
def preprocess_data(record, company, date):
    # calculate the features
    record["relative_day"] = get_relativeday(record.pop("date"))
    record = get_company_code(record, company)      
   	
    # return the necessary features
    result = []
    for key, value in record.items():
        if key in ["relative_day",
                   "company_amazon", "company_apple", "company_facebook", "company_google", 
                   "company_microsoft", "company_netflix", "company_tesla"]:
            result.append(value)
        elif key in ["3_day_sentiment_score", '7_day_sentiment_score']:
            result.append(value)
        else:
            pass
    # print(result)
    return np.array(result).reshape(1, -1)
            
def on_click(clf, x_test):
    y_pred = clf.predict(x_test) # a np.array
    return y_pred

if __name__ == "__main__":    
    # load the pretrained model
    clf = joblib.load("./models/clf_KNN_model.joblib")
    
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
    db_collection = db[company]
    record = db_collection.find_one({"date": date})
    
    # preprocess the data
    x_test = preprocess_data(record, company, date) 
    
    # do the prediction
    result = on_click(clf, x_test)    
    print(result[0])