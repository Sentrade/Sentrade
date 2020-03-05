#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pymongo 
from sshtunnel import SSHTunnelForwarder
from plotly.subplots import make_subplots

__author__ = "Davide Locatelli"
__status__ = "Prototype"

def Graph(ticker):

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
    db = db_client["sentrade_db"]
    sentiment_db = db_client["sentiment_data"]

    companies = {
            "AMZN" : "Amazon.com Inc.",
            "AAPL"  : "Apple Inc.", 
            "FB"    : "Facebook Inc.",
            "GOOG"  : "Alphabet Inc.",
            "MSFT"  : "Microsoft Corporation",
            "NFLX"  : "Netflix Inc.",
            "TSLA"  : "Tesla Inc.",
            "UBER"  : "Uber Technologies Inc."
    }
        
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

    graph = []

    if not ticker:

        graph.append(html.H3(
            "No ticker selected.",
            style={
                'margin-top':'0px',
                'textAlign':'center',
                'color':'#9C9C9C'
            }
        ))

    else:

        graph.append(dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3(
                            ticker,
                            style={
                                'font-size':'2.5em',
                                'textAlign':'left',
                                'color':'black'
                                }
                        ),
                    ],
                    width = "auto"
                ),
                dbc.Col(
                    [
                        html.H5(
                            companies[ticker],
                            style={
                                'font-size':'0.5em',
                                'margin-top': '55%',
                                'textAlign':'left',
                                'color':'grey'
                            }
                        )
                    ],
                    width = "auto"
                )
            ]
        ))

        stock_price_collection = db["stock_price"]
        sentiment_collection = sentiment_db[company_db_name[ticker]]

        close = []
        stock_date = []
        for record in stock_price_collection.find({"company_name":ticker}):
            close.append(record["close"])
            stock_date.append(record["date"])
        
        polarity = []
        sent_date = []
        for record in sentiment_collection.find():
            polarity.append(record["1_day_sentiment_score"])
            sent_date.append(record["date"])
        
        eth_close = go.Scatter(
            y = close,
            x = stock_date,
            name = "Close",
            mode = "lines",
            line=dict(color="#7a90e0")
        )
        
        # eth_polarity = go.Histogram(
        #     y = polarity,
        #     x = sent_date,
        #     name = "Sentiment",
        #     histnorm='probability',
        #     # barmode = 'relative',
        #     # range_y = [-1,1],
        #     marker=dict(color='#FFC300',)
        # )

        eth_polarity = go.Scatter(
            y = polarity,
            x = sent_date,
            name = "Sentiment",
            mode = "lines",
            line=dict(color="#FFC300")
        )
        
        # eth_polarity = go.Bar(
        #     x = sent_date, 
        #     y = polarity,
        #     marker_color='#FFC300',
        #     name='Sentiment')
        
        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(eth_close,secondary_y=False)
        fig.add_trace(eth_polarity,secondary_y=True)
        fig.update_layout(
            margin= {'b': 0, 'r': 10, 'l': 60, 't': 0},                   
            legend= {'x': 0},
            # barmode='group', # rm 
            xaxis=go.layout.XAxis(
                rangeslider=dict(
                    visible=False
                ),
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1D",
                            step="day",
                            stepmode="backward"),
                        dict(count=7,
                            label="1W",
                            step="day",
                            stepmode="backward"),
                        dict(count=1,
                            label="1M",
                            step="month",
                            stepmode="backward"),
                        dict(count=3,
                            label="3M",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6M",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="1Y",
                            step="year",
                            stepmode="backward"),
                        dict(label='ALL',step="all")
                    ]),
                    font=dict(
                        family="Arial",
                        size=16,
                        color="white"),
                    bgcolor="#BABABA",
                    activecolor='#949494',
                    x=0.35,
                    y=-0.13
                ),
                type="date"
            )
        )
        graph.append(dcc.Graph(figure=fig,style={'margin-top':'0','height':'400'}))
    return graph