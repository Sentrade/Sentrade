#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib


from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import  train_test_split
from sklearn.metrics import r2_score, mean_squared_error

__author__ = "Fengming Liu, Longzhen Li, Shaomiao Yin"
__status__ = "Development"

    
def regressor_run(reg, name, x_train, x_test, y_train, y_test):
    reg.fit(x_train,y_train)
    y_pred = reg.predict(x_test)   
    # print((y_pred - y_test)/y_test)
    return [r2_score(y_test, y_pred), np.sqrt(mean_squared_error(y_test, y_pred))]

##### Main #####
total_df = pd.read_csv("./total_data.csv")
response = "close"
features_list = [["relative_day", "company_amazon", "company_apple", "company_facebook", "company_google", 
                   "company_microsoft", "company_netflix", "company_tesla", "3_day_sentiment_score"],
                 ["relative_day", "company_amazon", "company_apple", "company_facebook", "company_google", 
                   "company_microsoft", "company_netflix", "company_tesla"],
                ]

result = open("./results/reg_results.csv", "w")
alg_dict = {"KNN": KNeighborsRegressor(),
            "DecisionTree": DecisionTreeRegressor(),
            "Linear": LinearRegression(),
            "Ridge": Ridge(),
            "Lasso": Lasso()
            }

# ML
for features in features_list:
    # record the information for each run
    result.write("features:,")
    for feat in features:
        result.write(feat + ',')
    result.write('\n')
    result.write("response:," + response + '\n')
    result.write(" ,")
    for alg_name, _ in alg_dict.items():
        result.write(alg_name + ',')
    result.write('\n')
    result.write(" ,")
    
    # prepare the data
    x_train, x_test, y_train, y_test = train_test_split(total_df[features].to_numpy(),
                                                        total_df[response],
                                                        test_size=0.3,
                                                        shuffle=True,
                                                        random_state=500)    
    # train the model
    for alg_name, reg in alg_dict.items():
        print("features:")
        print(features)
        [R2_score, RMSE] = regressor_run(reg, alg_name, x_train, x_test, y_train, y_test)
        result.write(str(R2_score) + " ,")
        print("algorithm:", alg_name)
        print("R2 score:", R2_score)
        print("RMSE:", RMSE)        
        print()
        joblib.dump(reg, "./models/reg_" + alg_name + "_model.joblib")
    result.write('\n')
result.write('\n\n')
result.close()
