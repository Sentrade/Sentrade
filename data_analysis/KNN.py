#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.model_selection import  train_test_split
from sklearn.metrics import accuracy_score

__author__ = "Fengming Liu"
__status__ = "Development"

    
def classifier_run(clf, name, x_train, x_test, y_train, y_test):
    clf.fit(x_train,y_train)
    y_pred = clf.predict(x_test)
    return accuracy_score(y_test, y_pred)


company_list = ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla"]
features_list = [["relative_day"],
                 ["past_3_days_senti_avg"],
#                 ["past_7_days_senti_avg"],
#                 ["1_day_sentiment_score"],
#                 ["1_day_news_count"],
#                 ["1_day_overall_sentiment_score"],
                 ["relative_day", "past_3_days_senti_avg"],
#                 ["relative_day", "past_7_days_senti_avg"]
                ]
response_list = ["up_cat"]
result = open("./KNN_results.csv", "w")

for response in response_list:
    for features in features_list:
        # write info
        result.write("features:,")
        for feat in features:
            result.write(feat + ',')
        result.write('\n')
        result.write("response:," + response + '\n')
        result.write('neighbors,')
        for company in company_list:
            result.write(company + ',')
        result.write('\n')
        
        # do ML
        for n_neighbors in range(3, 12):
            clf = KNeighborsClassifier(n_neighbors=n_neighbors)
            result.write(str(n_neighbors) + ',')
    
            for company in company_list:
                total_df = pd.read_csv("./processed_data/{0}_clf.csv".format(company))
                x_train, x_test, y_train, y_test = train_test_split(total_df[features].to_numpy(),
                                                                    total_df[response],
                                                                    test_size=0.3,
                                                                    shuffle=True,
                                                                    random_state=500)
                accuracy = classifier_run(clf, "KNN", x_train, x_test, y_train, y_test)
                result.write(str(accuracy) + ',')
            result.write('\n')
        result.write('\n')
    result.write('\n')
result.write('\n')
result.close()
