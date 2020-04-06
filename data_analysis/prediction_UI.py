#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import datetime
import pymongo

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.model_selection import  train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix


__author__ = "Fengming Liu"
__status__ = "Development"

def get_relativeday(date):
    rel_days = (date - datetime.date(2019, 1, 1)).days
    return rel_days

def get_senti_data(db_client, company):
    db_collection = db_client["current_sentiment_data"][company]
    record = db_collection.find_one()
    feature_values = []
    feature_values.append(get_relativeday(record["date"]))
    feature_values.append(get_company_code(company))
    feature_values.append(float(record["1_day_sentiment_score"]["$numberDouble"]))
    feature_values.append(int(record["1_day_news_count"]["$numberInt"]))
    feature_values.append(float(record["1_day_overall_sentiment_score"]["$numberDouble"]))
    feature_values.append(float(record["past_3_days_senti_avg"]["$numberDouble"]))
    feature_values.append(float(record["past_7_days_senti_avg"]["$numberDouble"]))
    return feature_values
            

def on_click(clf, x_test):
    y_pred = clf.predict(x_test) # a np.array
    return y_pred[0]

if __name__ == "__main__":
    # load the pretrained model
    clf = joblib.load("./model.joblib")
    
    # connect to the database
    db_client = pymongo.MongoClient("mongodb://admin:sentrade@127.0.0.1", 27017)
    
    # get the sentiment data for the company
    company = get_company()
    x_test = get_senti_data(db_client["sentiment_data"], company)
    
    # do the prediction
    result = on_click(clf, x_test)
    print(result)