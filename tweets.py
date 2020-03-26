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

        news = html.Div(
            children = [
                html.H3(
                    className = "p-news",
                    children = "Tweets",
                    style={
                        'font-family':'sans-serif',
                        'font-weight':'500',
                        'letter-spacing':'1.5px',
                        'font-size':'1.1rem',
                        'textAlign':'center',
                        'color':'black',
                        'position':'absolute',
                        'margin-top':'1%'
                    }
                ),
                html.Div(
                    className = "table-news",
                    children = [
                        html.Div(
                            children = [
                                html.Div(
                                    children = [
                                        html.A(
                                            className = "td-link",
                                            children = tweets[i],
                                            target = "_blank",
                                        )
                                    ],
                                    style={
                                        'font-size' : '0.8rem',
                                        'font-family' : 'sans-serif'
                                    }
                                )
                            ],
                            style=tweetstyle(tweets_polarity,i)
                        )
                        for i in range(max_num)
                    ],
                    style={
                        'margin-top' : '2%',
                        'padding-top':'8%',
                        'height':'592px',
                        'overflow-y':'scroll',
                        'display':'block',
                        'background-color': 'rgba(120,120,120,0.15)',
                        'border-radius':'5px',
                        'margin-right' : '5.5%'
                    }
                )
            ]
        )

    return news

def tweetstyle(tweets_polarity, i):
    style = {
        'background-color' : 'rgba(235,158,62,0.5)',
        'border-radius' : '5px',
        'margin-top':'1%'
        }
    if tweets_polarity[i] < -0.3:
        style = {
            'background-color' : 'rgba(233,82,82,0.5)',
            'border-radius' : '5px',
            'margin-top' : '1%'
        }
    if tweets_polarity[i] > 0.3:
        style = {
            'background-color' : 'rgba(9,168,17,0.5)',
            'border-radius' : '5px',
            'margin-top' : '1%'
        }
    return style