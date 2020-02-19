#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

        graph.append(html.H3(
            ticker,
            style={
                'font-size':'2.5em',
                'margin-left':'20px',
                'textAlign':'left',
                'color':'black'
            }
        ))
        stock_price_collection = db["stock_price"]
        sentiment_collection = db["news"]

        close = []
        stock_date = []
        for record in stock_price_collection.find({"company_name":ticker}):
            close.append(record["close"])
            stock_date.append(record["date"])
        """
        polarity = []
        sent_date = []
        for record in sentiment_collection.find():
            polarity.append(record["polarity"])
            sent_date.append(record["date"])
        """
        eth_close = go.Scatter(
            y = close,
            x = stock_date,
            name = "Close",
            mode = "lines",
            line=dict(color="#7a90e0")
        )
        """
        eth_polarity = go.Scatter(
            y = polarity,
            x = sent_date,
            name = "Sentiment",
            mode = "lines",
            line=dict(color="#FFC300")
        )
        """
        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(eth_close,secondary_y=False)
        #fig.add_trace(eth_polarity,secondary_y=True)
        fig.update_layout(
            margin= {'b': 0, 'r': 10, 'l': 60, 't': 0},                   
            legend= {'x': 0},
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