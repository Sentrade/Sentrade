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

aboutus = """This website aims to provide sentiment analysis of eight stocks by applying natural language processing on Twitter posts. 

This is a temporary website built by 6 MSc students from Imperial College London and it will be removed in June 2020. 

SenTrade makes no express or implied warranty that the website will be updated timely: please do not use it for trading purposes. 

SenTrade will not be liable for any damages or losses caused by the use of information provided."""

search_bar = dbc.Row(
    [
        dbc.Col([dbc.Button(
            "About", 
            className="button-about",
            id="modal-target", 
            color="secondary", 
            outline=True, 
            size="sm",
            style={
                "font-size":"0.765625rem",
                "font-family":"sans-serif",
                "font-weight":"350",
                "letter-spacing":"1px",
                "padding":"inherit",
                "color":"#aaa"
            }
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("About Sentrade"),
                dbc.ModalBody(aboutus,style={"white-space": "pre-line"}),
                dbc.ModalFooter(dbc.Button("Close",id="close",color="secondary", 
                    outline=True, 
                    size="sm",
                    style={
                        "font-size":"0.6rem",
                        "font-family":"sans-serif",
                        "font-weight":"350",
                        "width":'20%',
                        "letter-spacing":"1px",
                        "color":"#aaa"
                    })),
            ],
            id='modal-scroll',
            scrollable=True
        ),]),
        dbc.Col(dcc.Dropdown(
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
                        'margin-right' : '80px'
                    }
                ))
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Sentrade", className="ml-2")),
                    dbc.Col(html.H6("Financial Sentiment Analysis",style={"white-space":"nowrap","color":"grey","margin-top":"8px"}))
                ],
                align="center",
                no_gutters=True,
            ),
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    className = "navbar"
)

#news = html.Div(
 #   className= "div-news",
  #  children= [html.Div(id="news")]
#)

graph = html.Div(
    className = 'graph',
    id = 'graph',
    style={
        'margin-top':'0.8%'
    }
)

tweets = html.Div(
    className = 'tweets',
    id = 'tweets',
)

data = html.Div(
    className= 'finance',
    id = 'finance'
)

leftdiv = html.Div(
    [
        graph,
        data
    ]
)
contents = html.Div(
    className= 'contents',
    children= dbc.Row([
        dbc.Col(leftdiv,width=8),
        dbc.Col(tweets)
    ])
)

def MainPage():
    layout = html.Div([
        navbar,
        contents,
    ]
    )

    return layout

# App set up
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server
app.layout = MainPage()
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# App callbacks
@app.callback(
    dash.dependencies.Output('tweets','children'),
    [dash.dependencies.Input('stock-ticker', 'value')])
def update_tweets(ticker):
    return Tweets(ticker)

"""
@app.callback(
    dash.dependencies.Output('news','children'),
    [dash.dependencies.Input('stock-ticker', 'value')])
def update_tweets(ticker):
    return News(ticker)
"""
@app.callback(
    dash.dependencies.Output('graph','children'),
    [dash.dependencies.Input('stock-ticker', 'value')])
def update_graph(ticker):
    return Graph(ticker)

@app.callback(
    dash.dependencies.Output('finance','children'),
    [dash.dependencies.Input('stock-ticker', 'value')])
def update_finance(ticker):
    return F_data(ticker)

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("modal-scroll", "is_open"),
    [
        Input("modal-target", "n_clicks"),
        Input("close", "n_clicks"),
    ],
    [State("modal-scroll", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Debugging
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=80)
