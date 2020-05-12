#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import matplotlib.pyplot as plt
from pathlib import Path
import os

__author__ = "Yiwen Sun, Ziyou Zhang"
__status__ = "Development"

def data_study(company_name, client_address, field):

    # Setup the connection.
    client = MongoClient(client_address)

    # Use the database sentrade_db. Select the table to use.
    stock_db = client.stock_data[company_name]
    sentiment_db = client.sentiment_data[company_name]
    # get all data
    all_stock = stock_db.find().sort("date")
    all_sentiment = sentiment_db.find().sort("date")

    stock_date = []
    stock_open = []
    stock_close = []
    stock_change = []
    sentiment_date = []
    sentiment_score = []
    sentiment_overall = []

    for stock in all_stock:
        stock_date.append(stock["date"])
        stock_open.append(stock["open"])
        stock_close.append(stock["close"])
    
    # stock price difference between tomorrow's close and today's close
    for i in range(1, len(stock_date)):
        stock_change.append((stock_close[i] - stock_close[i-1])/stock_close[i-1] * 100)

    for sentiment in all_sentiment:
        sentiment_date.append(sentiment["date"])
        sentiment_score.append(sentiment[field])
    client.close()

    change_plot = []
    sentiment_plot = []
    sentiment_overall_plot = []
    for i in range(len(stock_date)):
        for j in range(len(sentiment_date)):
            if stock_date[i] == sentiment_date[j]:
                change_plot.append(stock_change[i])
                sentiment_plot.append(sentiment_score[j])
                # sentiment_overall_plot.append(sentiment_overall[j])
    
    # plt.plot(sentiment_plot, change_plot, 'k.')
    # plt.title(company_name)
    # plt.xlabel("1 day average sentiment score")
    # plt.ylabel("stock price change percentage / %")
    # plt.savefig(Path("./scatter/" + company_name + "_average.png"))
    # plt.clf()

    # plt.plot(sentiment_plot, change_plot, 'b.')
    # plt.title(company_name)
    # plt.xlabel("1 day average overall sentiment score")
    # plt.ylabel("stock price change")
    # plt.savefig(Path("/scatter/" + company_name + "_overall.png"))
    
    return sentiment_plot, change_plot

if __name__ == "__main__":
    import numpy as np

    client_address = "mongodb://admin:sentrade@45.76.133.175:27017"
    companies = ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]
    companies = ["microsoft"]

    for i in range(len(companies)):
        x, y = data_study(companies[i], client_address, "1_day_sentiment_score")
        # x, y = data_study(companies[i], client_address, "1_day_overall_sentiment_score")
        # x, y = data_study(companies[i], client_address, "1_day_bert_sentiment_score")
        # x, y = data_study(companies[i], client_address, "1_day_overall_bert_sentiment_score")
        array = np.asarray([x, y])
        filepath = Path("./data/{}.csv".format(companies[i]))
        np.savetxt(filepath, array, delimiter=",")
        print("saving data for", companies[i], "finished")

    # extreme score plot
    fig, axs = plt.subplots(nrows=2, ncols=4, figsize=[20, 10])
    for i in range(len(companies)):
        filepath = Path("./data/{}_outlier.csv".format(companies[i]))
        result = np.loadtxt(filepath, delimiter=",")
        axs[i//4, i%4].plot(result[0], result[1], '.', markersize=4)
        axs[i//4, i%4].set_xlim([-0.1, 0.6])
        axs[i//4, i%4].set_ylim([-10, 10])
        axs[i//4, i%4].set_xticks(np.arange(-0.05, 0.26, 0.05))
        axs[i//4, i%4].set_xticks(np.arange(-0.1, 0.61, 0.1))
        axs[i//4, i%4].set_yticks(np.arange(-10, 11, 5))
        axs[i//4, i%4].set_xlabel("{} past day sentiment (outlier)".format(companies[i]), fontsize=14)
    axs[0,0].set_ylabel("price change percentage", fontsize=14)
    axs[1,0].set_ylabel("price change percentage", fontsize=14)

    plt.savefig(Path("scatter_all_outlier.png"), dpi=500)

    # normal plot
    fig, axs = plt.subplots(nrows=2, ncols=4, figsize=[20, 10])
    for i in range(len(companies)):
        filepath = Path("./data/{}.csv".format(companies[i]))
        filepath = Path("./data/{}.csv".format(companies[i]))
        result = np.loadtxt(filepath, delimiter=",")
        axs[i//4, i%4].plot(result[0], result[1], '.', markersize=4)
        axs[i//4, i%4].set_xlim([-0.05, 0.25])
        axs[i//4, i%4].set_ylim([-10, 10])
        axs[i//4, i%4].set_xticks(np.arange(-0.05, 0.26, 0.05))
        axs[i//4, i%4].set_yticks(np.arange(-10, 11, 5))
        axs[i//4, i%4].set_xlabel("{} past day sentiment".format(companies[i]), fontsize=14)
    axs[0,0].set_ylabel("price change percentage", fontsize=14)
    axs[1,0].set_ylabel("price change percentage", fontsize=14)

    plt.savefig(Path("scatter_all.png"), dpi=500)

    # single company plot
    result = np.loadtxt("./data/microsoft_outlier.csv", delimiter=",")
    plt.plot(result[0], result[1], '.', markersize=4)
    plt.rcParams["figure.figsize"]= (3,2)
    plt.xlabel("sentiment score (extreme score only)",  fontsize=14)
    plt.ylabel("price change percentage",  fontsize=14)
    plt.savefig(Path("microsoft_init_outlier.png"), dpi=500)
