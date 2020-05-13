#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import  train_test_split
from sklearn.metrics import r2_score

__author__ = "Fengming Liu"
__status__ = "Development"

    
def regressor_run(reg, name, x_train, x_test, y_train, y_test):
    reg.fit(x_train,y_train)
    y_pred = reg.predict(x_test)
    
    print(name)
    print("R2:", r2_score(y_test, y_pred))
#    print("RMSE:", mean_squared_error(y_test, y_pred))
    
    plt.plot(y_test, label='true')
    plt.plot(y_pred, label='pred')
    plt.legend()
    plt.title(name)
    plt.show()
    return r2_score(y_test, y_pred)


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
response_list = ["high", "low", "open", "close", "volume"]
result = open("./basic_models_results.csv", "a")
alg_dict = {"KNN": KNeighborsRegressor(),
            "DecisionTree": DecisionTreeRegressor(),
#            "Linear": LinearRegression(),
#            "Ridge": Ridge(),
#            "Lasso": Lasso()
            }

for response in response_list:
    for features in features_list:
        result.write("features:,")
        for feat in features:
            result.write(feat + ',')
        result.write('\n')
        result.write("response:," + response + '\n')
        result.write(" ,KNN,DecisionTree,Linear,Ridge,Lasso\n")
        for company in company_list:
            total_df = pd.read_csv("./processed_data/{0}.csv".format(company))
            x_train, x_test, y_train, y_test = train_test_split(total_df[features].to_numpy(),
                                                                total_df[response].to_numpy(dtype=np.float32),
                                                                test_size=0.3,
                                                                shuffle=True,
                                                                random_state=500)
            result.write(company + ',')
            for alg_name, reg in alg_dict.items():
                print(alg_name)
                print(features)
                print(response)
                Rsquared_score = regressor_run(reg, alg_name, x_train, x_test, y_train, y_test)
                result.write(str(Rsquared_score))
                result.write(',')
            result.write('\n')
        result.write('\n')
        break
    result.write('\n')
    break
result.write('\n')
result.close()
