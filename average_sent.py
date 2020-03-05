#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pymongo
import requests
import pandas as pd
import datetime as dt
import statistics
import dash_html_components as html

from sshtunnel import SSHTunnelForwarder

__author__ = "Davide Locatelli"

def Score(ticker):

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
    db = db_client["sentrade_db"]

    max_rows = 10
    
    if not ticker:

        polarity = html.H3(
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

        polarity_string = "Average sentiment for " + ticker
        polarity_string += " on SEPT 16"
        polarity_avg = statistics.mean(tweets_polarity)
        polarity_avg_string = str(polarity_avg)
        polarity = html.Div([
            html.Div([html.H3(polarity_string)]),
            html.Div([html.P(polarity_avg_string)],style=score_style(polarity_avg)),
            ]
        )

    return polarity

def score_style(polarity_avg):
    style = { 'color' : '#e0d204' }
    if polarity_avg < -0.3:
        style = {
            'color' : 'red'
        }
    if polarity_avg > 0.3:
        style = {
            'color' : 'green'
        }
    return style