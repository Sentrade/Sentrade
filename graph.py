#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pymongo 
from sshtunnel import SSHTunnelForwarder
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from prediction import Prediction

__author__ = "Davide Locatelli"
__status__ = "Prototype"

def Graph(ticker):

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)

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

        graph.append(html.H6(
            "No ticker selected.",
            style={
                'margin-top':'35%',
                'margin-left':'50%',
                'textAlign':'center',
                'color':'#9C9C9C'
            }
        ))

    else:

        row = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(html.H3(ticker, style={
                                'font-family':'sans-serif',
                                'font-weight':'500',
                                'letter-spacing':'1.5px',
                                'font-size':'1.1rem',
                                'textAlign':'center',
                                'color':'black',
                                'position':'absolute',
                                'margin-left': '44.4%',
                                'margin-top' : '5%'
                                }),width=1),
                        dbc.Col(html.H6(companies[ticker], style={
                                'font-size':'0.75rem',
                                'textAlign':'left',
                                'margin-top':'0.8%',
                                'margin-left': '106%',
                                'color':'grey',
                                'white-space':'nowrap',
                                'font-weight': '600'
                            }),width=2),
                        dbc.Col(Prediction(ticker), style={
                                'margin-left':'52%'
                        })
                    ]
                ),
            ]
)

        graph.append(row)

        stock_price_db = db_client.sentrade_db.stock_price
        sentiment_db = db_client.sentiment_data[company_db_name[ticker]]

        close = []
        stock_date = []
        for record in stock_price_db.find({"company_name":ticker}):
            close.append(record["close"])
            stock_date.append(record["date"])
        
        polarity = []
        sent_date = []
        for record in sentiment_db.find().sort("date"):
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
        
        #eth_polarity = go.Bar(
         #   x = sent_date, 
          #  y = polarity,
           # marker_color='#FFC300',
            #name='Sentiment')
        
        yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
        three_months_ago = (datetime.now() - timedelta(92)).strftime('%Y-%m-%d')

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
                range= ["2018-11-01","2019-09-30"],
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
                            stepmode="backward"
                            ),
                        dict(count=1,
                            label="1Y",
                            step="year",
                            stepmode="backward"),
                        dict(label='ALL',
                        step="all")
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
        graph.append(dcc.Graph(id='click-graph',figure=fig,style={'margin-top':'0.6%'}))
    return graph