#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pymongo
import requests
import pandas as pd
import datetime as dt
import dash_html_components as html

from sshtunnel import SSHTunnelForwarder

__author__ = "Davide Locatelli"

def Tweets(ticker):

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
    db = db_client["sentrade_db"]

    max_num = 10
    
    if not ticker:

        news = html.H3(
            "No ticker selected.",
            style={
                'margin-top':'0px',
                'textAlign':'center',
                'color':'#9C9C9C'
            }
        )

    else:
        companies = {
            "AMZN" : "Amazon",
            "AAPL"  : "Apple", 
            "FB"    : "Facebook",
            "GOOG"  : "Google",
            "MSFT"  : "Microsoft",
            "NFLX"  : "Netflix",
            "TSLA"  : "Tesla",
            "UBER"  : "Uber"
        }

        twitter_collection = db["news"]
        tweets = []
        tweets_polarity = []
        for record in twitter_collection.find({"company" : companies[ticker]}):
            tweets.append(record["text"])
            tweets_polarity.append(record["polarity"])

        news = html.Div(
            children = [
                html.H3(
                    className = "p-news",
                    children = "Tweets on SEPT 16"
                ),
                html.Table(
                    className = "table-news",
                    children = [
                        html.Tr(
                            children = [
                                html.Td(
                                    children = [
                                        html.A(
                                            className = "td-link",
                                            children = tweets[i],
                                            target = "_blank",
                                            style = tweetstyle(tweets_polarity, i)
                                        )
                                    ]
                                )
                            ]
                        )
                        for i in range(max_num)
                    ] 
                )
            ]
        )

    return news

def tweetstyle(tweets_polarity, i):
    style = { 'color' : '#e0d204' }
    if tweets_polarity[i] < -0.3:
        style = {
            'color' : 'red'
        }
    if tweets_polarity[i] > 0.3:
        style = {
            'color' : 'green'
        }
    return style