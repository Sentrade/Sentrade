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
        company_db_name = {
            "AMZN" : "amazon",
            "AAPL"  : "apple", 
            "FB"    : "facebook",
            "GOOG"  : "google",
            "MSFT"  : "microsoft",
            "NFLX"  : "netflix",
            "TSLA"  : "tesla",
            "UBER"  : "uber"
        }
        
        db = db_client.sentiment_data[company_db_name[ticker]]
        scores = []
        dates = []
        for record in db.find():
            scores.append(record["1_day_sentiment_score"])
            dates.append(record["date"])

        polarity_values = []
        for score in scores:
            polarity_value = score + 1
            polarity_value /= 2
            polarity_value *= 100
            polarity_values.append(polarity_value)

        polarity_value = polarity_values[-1]
        polarity_value_string = "{:.0f}%".format(polarity_value) 
        polarity = html.Div([
            html.Div(dbc.Progress(polarity_value_string, value=polarity_value, color=score_style(scores[-1]),className="mb-3")),
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