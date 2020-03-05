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
from financial_data import F_data
from graph import Graph
from tweets import Tweets
from news import News
from average_sent import Score

__author__ = "Davide Locatelli"
__status__ = "Prototype"

# App layout
navbar = dbc.NavbarSimple(
        children = [
            dbc.NavItem(
                dbc.NavLink(
                    "Financial Sentiment Analysis",
                    href = "/about",
                    style = {
                        'margin-right' : '650px'
                    }
                )
            ),
            dbc.NavItem(
                dcc.Dropdown(
                    id = 'stock-ticker',
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

sidebar = html.Div(
            className="sidebar",
            children=[
                html.H1(className="title-header", children="SENTRADE"),
                html.P(
                    """
                    This app lets you explore the correlation between financial and sentiment
                    analysis.
                    """
                ),
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
                ),
                html.Div(
                className="div-news",
                children=[html.Div(id="news")],
                ),
            ]
)

graph = html.Div(
    className = 'graph',
    id = 'graph',
)

tweets = html.Div(
    className = 'tweets',
    id = 'tweets',
)

financial_data = html.Div(
    className= 'finance',
    id = 'finance'
)

sentiment_data = html.Div(
    className= 'sentiment',
    id = 'sentiment'
)

contents = html.Div(
    className= 'contents',
    children= [
        graph,
        financial_data,
        tweets,
        sentiment_data
    ]
)

def MainPage():
    layout = html.Div([
        sidebar,
        contents,
    ],
    style={'display':'flex'})

    return layout

# App set up
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = MainPage()
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# App callbacks
@app.callback(
    dash.dependencies.Output('tweets','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value')])
def update_tweets(ticker):
    return Tweets(ticker)

@app.callback(
    dash.dependencies.Output('news','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value')])
def update_tweets(ticker):
    return News(ticker)

@app.callback(
    dash.dependencies.Output('graph','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value')])
def update_graph(ticker):
    return Graph(ticker)

@app.callback(
    dash.dependencies.Output('finance','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value')])
def update_finance(ticker):
    return F_data(ticker)

@app.callback(
    dash.dependencies.Output('sentiment','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value')])
def update_finance(ticker):
    return Score(ticker)

"""
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
"""

# Debugging
if __name__ == "__main__":
    app.run_server(debug=True)#, host='0.0.0.0', port=80)