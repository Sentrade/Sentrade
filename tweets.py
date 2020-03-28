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
        
        db = db_client.twitter_data[company_db_name[ticker]]

        tweets = []
        tweets_polarity = []
        for record in db.find():
            tweets.append(record["original_text"])
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
                        'textAlign':'left',
                        'color':'black',
                        'position':'relative',
                        'margin-top':'1.2%',
                        'margin-left' : '1%'
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
                        for i in range(100)
                    ],
                    style={
                        'margin-left' :'1%',
                        'margin-right': '1%',
                        'margin-bottom': '1%'
                    }
                )
            ],
            style={
                'background-color': 'rgba(120,120,120,0.15)',
                'border-radius':'5px',
                'margin-right' : '5.5%',
                'overflow':'scroll',
                'display':'block',
                'margin-top' : '1.3%',
                'height':'597px'
            }
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