#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.model_selection import  train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, plot_confusion_matrix

__author__ = "Fengming Liu, Longzhen Li, Shaomiao Yin"
__status__ = "Development"

    
def classifier_run(clf, name, x_train, x_test, y_train, y_test):
    clf.fit(x_train,y_train)
    y_pred = clf.predict(x_test)
    return [accuracy_score(y_test, y_pred), clf]

def write_result(csv_file, alg_name, accuracy, cm, n_cat=5):
    result.write(alg_name + ',' + str(accuracy) + ',\n')
    for i in range(n_cat):
        for j in range(n_cat):
            result.write(str(cm[i][j]) + ',')
        result.write('\n')
    result.write('\n')


##### Main #####
total_df = pd.read_csv("./total_data.csv")
total_df.dropna(inplace=True)
response = "up_cat"
fea_date_company = ["relative_day", "company_amazon", "company_apple", 
                    "company_facebook", "company_google", "company_microsoft", 
                    "company_netflix", "company_tesla"]
features_list = [fea_date_company + ["7_day_sentiment_score"],
                 fea_date_company + ["7_day_bert_sentiment_score"],
                 fea_date_company + ["3_day_sentiment_score"],
                 fea_date_company + ["3_day_bert_sentiment_score"],
                 ]


result = open("./results/clf_results.csv", "w")
alg_dict = {"KNN": KNeighborsClassifier(n_neighbors = 3,weights = 'distance',n_jobs = -1),
            "DecisionTree": DecisionTreeClassifier(criterion='entropy',max_depth=10,min_samples_leaf=5),
            "SVM": SVC(kernel='linear', gamma='auto'),
            }

# ML
for features in features_list:
    # record the information for each run
    result.write("features:,")
    for feat in features:
        result.write(feat + ',')
    result.write('\n')
    result.write("response:," + response + '\n')
    result.write(" ,\n")
    
    # prepare the data
    x_train, x_test, y_train, y_test = train_test_split(total_df[features].to_numpy(),
                                                        total_df[response],
                                                        test_size=0.3,
                                                        shuffle=True,
                                                        random_state=500)    
    # train the model
    for alg_name, clf in alg_dict.items():
        [accuracy, clf] = classifier_run(clf, alg_name, x_train, x_test, y_train, y_test)
        disp = plot_confusion_matrix(clf, x_test, y_test,
                                     display_labels=[-2, -1, 0, 1, 2],
                                     cmap=plt.cm.Blues)
        disp.ax_.set_title(alg_name)
        plt.savefig("./results/{0}.png".format(alg_name))
        
        print("distinct features:", features)
        print("algorithm:", alg_name)
        print("accuracy:", accuracy)
        print(disp.confusion_matrix)
        print()
        
        joblib.dump(clf, "./models/clf_" + alg_name + "_model.joblib")
        write_result(result, alg_name, accuracy, disp.confusion_matrix)
    result.write('\n')
result.write('\n\n')
result.close()
