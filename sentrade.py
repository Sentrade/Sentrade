#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import chart_studio.plotly as py
import plotly.graph_objs as go
import requests
import pandas as pd
import json
import datetime as dt
import colorlover as cl
import datetime as dt
import flask
import os
import pymongo 
from sshtunnel import SSHTunnelForwarder
from plotly.subplots import make_subplots

from textwrap import dedent as d
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from plotly import tools
from data import correlation_analysis
from graph import Graph
from news import News

__author__ = "Davide Locatelli"
__status__ = "Prototype"

navbar = dbc.NavbarSimple(
        children = [
            dbc.NavItem(
                dbc.NavLink(
                    "Financial Sentiment Analysis",
                    href = "/about",
                    style = {
                        'margin-right' : '1269px'
                    }
                )
            ),
            dbc.NavItem(
                dcc.Dropdown(
                    id = 'stock-ticker-input',
                    options = [
                        {"label" : "AAPL" , "value" : "AAPL"},
                        {"label" : "AMZN" , "value" : "AMZN"},
                        {"label" : "FB"   , "value" : "FB"  },
                        {"label" : "GOOG" , "value" : "GOOG"},
                        {"label" : "MSFT" , "value" : "MSFT"},
                        {"label" : "NFLX" , "value" : "NFLX"},
                        {"label" : "TSLA" , "value" : "TSLA"},
                        {"label" : "UBER" , "value" : "UBER"},
                    ],
                    placeholder = "Select Ticker",
                    multi = False,
                    style = {
                        "width" : "100%",
                        'margin-right' : '100px'
                    }
                )
            )
        ],
        brand = "Sentrade",
        brand_href = "/home",
        sticky = "top",
        fluid = True,
)

graph = html.Div(
    className = 'graph',
    id = 'graph',
)

news = html.Div(
    className = 'news',
    id = 'news',
)

contents = html.Div(
    className = 'contents',
    children = [
        graph,
        news
    ]
)

def MainPage():
    layout = html.Div([
        navbar,
        contents
    ])

    return layout

app = dash.Dash(__name__, meta_tags=[{"name":"viewport", "content": "width=device-width"}])
server = app.server
app.layout = MainPage()

@app.callback(
    dash.dependencies.Output('news','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value')])
def update_news(ticker):
    return News(ticker)

@app.callback(
    dash.dependencies.Output('graph','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value')])
def update_graph(ticker):
    return Graph(ticker)

if __name__ == "__main__":
    app.run_server(debug=True)#, host='0.0.0.0', port=80)