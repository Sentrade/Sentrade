#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import requests
import datetime as dt
import pandas as pd
from textblob import TextBlob

'''
response = requests.get('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'from=2020-01-20&'
       'sortBy=popularity&'
       'apiKey=954c05db19404ee99531875f66d9d138')
'''
def News(ticker):
    if not ticker:
        return html.Div(
            [html.H3(
                "",
                style={
                    'margin-top':'0px',
                    'textAlign':'center',
                    'color':'#9C9C9C'
                }
            )]
        )
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
    request_string = 'https://newsapi.org/v2/everything?q='
    request_string += companies[ticker]
    request_string += '&from=2020-02-24&sortBy=popularity&language=en&'
    request_string += 'apiKey=13ac274ab9a140f5a052721187a8d0ef'
    response = requests.get(request_string)
    articles = response.json()["articles"]
    df = pd.DataFrame(articles)
    df = pd.DataFrame(df[["title","url"]])
    max_rows = 10
    return html.Div(
        children =[
            html.H3(className="p-news",children="Headlines"),
            html.P(
                className="p-news-float-left",
                children="Last update: "
                + dt.datetime.now().strftime("%H:%M:%S")
            ),
            html.Table(
                className="table-news",
                children= [
                    html.Tr(
                        children=[
                            html.Td(
                                children=[
                                    html.A(
                                        className="td-link",
                                        children=df.iloc[i]["title"],
                                        style= newsStyle(df.iloc[i]["title"]),
                                        href=df.iloc[i]["url"],
                                        target="_blank",
                                    )
                                ]
                            )
                        ]
                    )
                    for i in range(min(len(df),max_rows))
                ],
            ),
        ]
    )

def newsStyle(news_title):
    analysis = TextBlob(news_title)
    style = { 'color' : '#e0d204' }
    if analysis.sentiment.polarity < -0.3:
        style = {
            'color' : 'red'
        }
    if analysis.sentiment.polarity > 0.3:
        style = {
            'color' : 'green'
        }
    return style