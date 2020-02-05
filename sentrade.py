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

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from plotly import tools
from data import correlation_analysis

__author__ = "Davide Locatelli, Longzhen Li, Ziyou Zhang"
__status__ = "Prototype"

app = dash.Dash(__name__, meta_tags=[{"name":"viewport", "content": "width=device-width"}])
server = app.server

colorscale = cl.scales['9']['qual']['Paired']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/dash-stock-ticker-demo.csv')

#load news
#this is just for apple, we can change according to the ticker inserted
response = requests.get('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'from=2020-01-20&'
       'sortBy=popularity&'
       'apiKey=954c05db19404ee99531875f66d9d138')
#print (response.json())

def update_news():
    articles = response.json()["articles"]
    df = pd.DataFrame(articles)
    df = pd.DataFrame(df[["title","url"]])
    max_rows = 10
    return html.Div(
        children =[
            html.P(className="p-news",children="Headlines"),
            html.P(
                className="p-news-float-right",
                children="Last update: "
                + datetime.datetime.now().strftime("%H:%M:%S")
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

app.layout = html.Div(
    children=[
        html.Div(
            className='top-bar',
            children=[
                html.H2(
                    'SENTRADE',
                    style={'display': 'inline',
                    'float': 'left',
                    'font-size': '2.65em',
                    'margin-left': '7px',
                    'font-weight': '900',
                    'font-family': 'Product Sans',
                    'color': 'black',
                    'margin-top': '20px',
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
                    'margin-top': '29px',
                    'margin-bottom': '0'
                    }
                ),
                dcc.Dropdown(
                    id='stock-ticker-input',
                    options=[
                        {'label':'AMZN','value':'AMZN','disabled':True},
                        {'label':'AAPL','value':'AAPL', 'disabled':False},
                        {'label':'FB','value':'FB','disabled':True},
                        {'label':'GOOG','value':'GOOG','disabled':True},
                        {'label':'MSFT','value':'MSFT','disabled':True},
                        {'label':'NFLX','value':'NFLX','disabled':True},
                        {'label':'TSLA','value':'TSLA','disabled':False},
                        {'label':'UBER','value':'UBER','disabled':True},
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
                    'margin-top': '12px'
                    }
                )
            ]
        ),
        html.Div(
            className='graphs',
            id='graphs',
            style={'width':'55%','float':'center'}
            )
    ]
)

def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std  = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value')])
def update_graph(ticker):
    graphs = []

    if not ticker:
        graphs.append(html.H3(
            "Select a stock ticker.",
            style={
                'textAlign':'center',
                'color':'#9C9C9C'
            }
        ))
    else:
        graphs.append(html.H3(
            "AAPL",
            style={
                'font-size':'2.5em',
                'textAlign':'left',
                'color':'black'
            }
        ))
        dff = df[df['Stock'] == ticker]
        candlestick = {
            'x': dff['Date'],
            'open': dff['Open'],
            'high': dff['High'],
            'low': dff['Low'],
            'close': dff['Close'],
            'type': 'candlestick',
            'name': ticker,
            'legendgroup': ticker,
            'increasing': {'line': {'color': colorscale[0]}},
            'decreasing': {'line': {'color': colorscale[1]}}
            }
        bb_bands = bbands(dff.Close)
        bollinger_traces = [{
            'x': dff['Date'], 'y': y,
            'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': colorscale[(i*2) % len(colorscale)]},
            'hoverinfo': 'none',
            'legendgroup': ticker,
            'showlegend': True if i == 0 else False,
            'name': '{} - bollinger bands'.format(ticker)
            } for i, y in enumerate(bb_bands)]
        graphs.append(dcc.Graph(
            id=ticker,
            figure={
                'data': [candlestick] + bollinger_traces,
                'layout': {
                'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                'legend': {'x': 0}
                }
            }
        ))

    return graphs
"""
    # Graph and news
    html.Div(
        className="two columns panel",
        children=[
            # Div for Graph
            html.Div(
                dcc.Graph(
                    id='output-graph',
                    figure={
                        'data': [
                            {'x': [], 'y': [], 'type': 'scatter', 'name': 'stock', 'mode': 'markers'},
                        ],
                        'layout': {
                            'title': 'stock sentiment',
                            'xaxis': {
                                'title':'sentiment_score'
                                },
                            'yaxis': {
                                'title':'stock_price_change'
                            }
                        }
                    },
                    style={
                        'width':'100%'
                        }
                )
            ),
            # Div for News Headlines
            html.Div(
                className="div-news",
                children=[html.Div(id="news", children=update_news())], 
                style={'width':'50%'}
            ), 
        ], 
        style={'columnCount': 2, 'width':'100%'}
    ),

html.Div(className="inputbox",children=[dcc.Input(id='input-box', value='', type='text'),html.Button('Submit', id='button'),], style={'width':'50%'}),


@app.callback(
    Output('output-graph', 'figure'),
    [Input('button', 'n_clicks')],
    [State('input-box', 'value')]
    )
def update_graph(no_clicked,input_value):

    sentiment_scores, price_changes = correlation_analysis("temp_twitter.json", "temp_sentiment.json", "temp_stock.json")

    if no_clicked is None:
         raise PreventUpdate
    elif input_value is None:
         raise PreventUpdate
    else: 
        return {  
        'data': [
                {'x': sentiment_scores, 'y': price_changes, 'type': 'scatter', 'name': 'stock', 'mode': 'markers', 'marker': {'size': 12}},
                ],
        'layout': {
            'title': 'stock sentiment',
            'xaxis': {
                'title':'sentiment_score'
            },
            'yaxis': {
                'title':'stock_price_change'
            }
            }           
        }
"""
if __name__ == "__main__":
    app.run_server(debug=True)