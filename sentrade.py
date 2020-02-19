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

app = dash.Dash(__name__, meta_tags=[{"name":"viewport", "content": "width=device-width"}])
server = app.server

app.layout = html.Div(
    children=[
        html.Div(
            className='top-bar',
            children=[
                html.H2(
                    'SENTRADE',
                    style={'display': 'inline',
                    'float': 'left',
                    'font-size': '3em',
                    'margin-left': '7px',
                    'font-weight': '900',
                    'font-family': 'Product Sans',
                    'color': 'black',
                    'margin-top': '0px',
                    'margin-bottom': '0'
                    }
                ),
                html.H4(
                    'Financial Sentiment Analysis',
                    style={'display': 'inline',
                    'float': 'left',
                    'font-size': '1.8em',
                    'margin-left': '7px',
                    'font-weight': '500',
                    'font-family': 'Product Sans',
                    'color': '#9C9C9C',
                    'margin-top': '14px',
                    'margin-bottom': '0'
                    }
                ),
                dcc.Dropdown(
                    id='stock-ticker-input',
                    options=[
                        {'label':'AMZN','value':'AMZN'},
                        {'label':'AAPL','value':'AAPL'},
                        {'label':'FB','value':'FB'},
                        {'label':'GOOG','value':'GOOG'},
                        {'label':'MSFT','value':'MSFT'},
                        {'label':'NFLX','value':'NFLX'},
                        {'label':'TSLA','value':'TSLA'},
                        {'label':'UBER','value':'UBER'},
                    ],
                    multi=False,
                    placeholder ='Select Ticker',
                    style={'display': 'inline',
                    'width':'35%',
                    'float': 'right',
                    'font-size': '1.2em',
                    'font-weight': '500',
                    'font-family': 'Product Sans',
                    'color': '#9C9C9C',
                    'margin-top': '6px'
                    }
                )
            ]
        ),
        html.Div(
            className= 'wrapper',
            children= [
                html.Div(
                    className = 'left-bar',
                    children = [
                        html.Div(
                            className='graph',
                            id='graph',
                        ),
                        html.Div(
                            className='click-data',
                            children= [
                                dcc.Markdown(d("""Financial Data""")),
                                html.Pre(id='click-data'),
                            ],
                        ),
                    ]
                ),
                html.Div(
                    className = 'right-bar',
                    children = [
                        html.Div(
                            className = 'news-bar',
                            id = 'news',
                        )
                    ]
                )
            ]
        )
    ]
)

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