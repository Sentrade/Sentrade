#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pymongo
import requests
import pandas as pd
import datetime as dt
import statistics
import dash_html_components as html
import dash_bootstrap_components as dbc

from sshtunnel import SSHTunnelForwarder

__author__ = "Davide Locatelli"

def Score(ticker):

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
    db = db_client["sentrade_db"]

    max_rows = 10
    
    if not ticker:

        polarity = html.H3(
            "",
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

        polarity_avg = statistics.mean(tweets_polarity)
        polarity_value = polarity_avg + 1
        polarity_value /= 2
        polarity_value *= 100
        polarity_value_string = "{:.0f}%".format(polarity_value) 
        polarity = html.Div([
            html.Div(dbc.Progress(polarity_value_string, value=polarity_value, color=score_style(polarity_avg),className="mb-3")),
            ]
        )

    return polarity

def score_style(polarity_avg):
    color = 'warning'
    if polarity_avg < -0.3:
        color = 'danger'
    if polarity_avg > 0.3:
        color = 'success'
    return color