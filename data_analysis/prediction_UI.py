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

    print("Feature values:", result)
    return np.array(result).reshape(1, -1)
            
def on_click(clf, x_test):
    y_pred = clf.predict(x_test) # a np.array
    return y_pred

def trial(db, company, date):
    print(company, date)

    # fetch the data from the database
    db_collection = db[company]
    record = db_collection.find_one({"date": date})
    if not record:
        print(company, date, "no record\n")
        return

    # preprocess the data
    distinct_features = ["7_day_sentiment_score"]
    x_test = preprocess_data(record, company, date, distinct_features) 
    
    # do the prediction
    result = on_click(clf, x_test)    
    print("Result:", result[0], '\n')

if __name__ == "__main__":    
    # load the pretrained model
    clf = joblib.load("./models/models_v2/clf_KNN_model.joblib")
    
    # connect to the database
    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
    db = db_client["sentiment_current"]
    
    trial(db, "apple", "2020-04-18")
    trial(db, "amazon", "2020-04-18")
    trial(db, "facebook", "2020-04-18")
    trial(db, "google", "2020-04-18")
    trial(db, "microsoft", "2020-04-18")
    trial(db, "netflix", "2020-04-18")
    trial(db, "tesla", "2020-04-18")
    trial(db, "uber", "2020-04-18")