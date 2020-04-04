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
                 ["past_7_days_senti_avg"],
                 ["1_day_sentiment_score"],
                 ["1_day_news_count"],
                 ["1_day_overall_sentiment_score"],
                 ["relative_day", "past_3_days_senti_avg"],
                 ["relative_day", "past_7_days_senti_avg"]
                ]
response_list = ["up_cat"]
result = open("./clf_results.csv", "a")
alg_dict = {"KNN": KNeighborsClassifier(),
            "DecisionTree": DecisionTreeClassifier(),
            "SMV": SVC(gamma='auto'),
            }

for response in response_list:
    for features in features_list:
        # write info
        result.write("features:,")
        for feat in features:
            result.write(feat + ',')
        result.write('\n')
        result.write("response:," + response + '\n')
        result.write(" ,")
        for alg_name, clf in alg_dict.items():
            result.write(alg_name + ',')
        result.write('\n')
        
        # do ML
        for company in company_list:
            total_df = pd.read_csv("./processed_data/{0}_clf.csv".format(company))
            x_train, x_test, y_train, y_test = train_test_split(total_df[features].to_numpy(),
                                                                total_df[response].to_numpy(dtype=np.float32),
                                                                test_size=0.3,
                                                                shuffle=True,
                                                                random_state=500)
            result.write(company + ',')
            for alg_name, clf in alg_dict.items():
                print(features, response, alg_name)
                accuracy = classifier_run(clf, alg_name, x_train, x_test, y_train, y_test)
                result.write(str(accuracy) + ',')
            result.write('\n')
        result.write('\n')
    result.write('\n')
result.write('\n')
result.close()
