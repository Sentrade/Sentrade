#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import joblib
import datetime
import pymongo

__author__ = "Fengming Liu"
__status__ = "Development"

def preprocess_data(record, company, date, distinct_features):
    # calculate the features
    [year, month, day] = date.split('-')
    record["relative_day"] = (datetime.date(int(year), int(month), int(day)) - datetime.date(2019, 1, 1)).days
    for name in ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]:
        record["company_"+name] = 0
    record["company_" + company] = 1
       
    # return the necessary features
    feat_date_company = ["relative_day", "company_amazon", "company_apple", 
                         "company_facebook", "company_google", "company_microsoft", 
                         "company_netflix", "company_tesla", "company_uber"]
    result = []
    for key, value in record.items():
        if key in distinct_features + feat_date_company:
            result.append(value)

    return np.array(result).reshape(1, -1)
            
def on_click(clf, x_test):
    y_pred = clf.predict(x_test) # a np.array
    return y_pred

def get_prediction(company, date):
    
    db_client = pymongo.MongoClient(os.environ["CLIENT_ADDR"])
    db = db_client["sentiment_current"]
    clf = joblib.load("data_analysis/models/clf_KNN_model.joblib")

    # fetch the data from the database
    db_collection = db[company]
    record = db_collection.find_one({"date": date})
    if not record:
        return -5

    # preprocess the data
    distinct_features = ["7_day_sentiment_score"]
    x_test = preprocess_data(record, company, date, distinct_features) 
    
    # do the prediction
    result = on_click(clf, x_test)    
    return int(result[0])

if __name__ == "__main__":
    score = get_prediction("amazon","2020-04-18")
    print(score)