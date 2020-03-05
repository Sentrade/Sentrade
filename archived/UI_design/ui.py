#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import chart_studio.plotly as py
import plotly.graph_objs as go
import requests
import pandas as pd
import json
import datetime

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from plotly import tools

__author__ = "Davide Locatelli, Longzhen Li"
__status__ = "Prototype"

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, meta_tags=[{"name":"viewport", "content": "width=device-width"}], external_stylesheets=external_stylesheets)
server = app.server

#load data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

tickers = ["AAPL"]

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
            className="top-bar",
            children=[
                html.H6(className="title-header", children="SENTRADE"),
                html.P(
                    """
                    Sentiment analysis of financial news data and twitter.
                    """
                )
            ], style={'textAlign': 'center'}
        ),

         html.Div(
            className="label",
            children=[
                html.Label('Stock ticker:',style={
                    'textAlign': 'center'}
                    ),
            ], style={'width':'20%'}
        ),

        html.Div(
            className="inputbox",
            children=[
                dcc.Input(id='input-box', value='', type='text'),
                html.Button('Submit', id='button'),
            ], style={'width':'50%'}
        ),

        
        # Graph and news
        html.Div(
            className="two columns panel",
            children=[
                # Div for Graph
                html.Div(id='output-graph', style={
                    'width':'100%'
                    }),
                # Div for News Headlines
                html.Div(
                    className="div-news",
                    children=[html.Div(id="news", children=update_news())
                    ], style={'width':'50%'}
                ), 
            ], style={'columnCount': 2, 'width':'100%'}
        ),
    ] 
)


@app.callback(
    Output('output-graph', 'children'),
    [Input('button', 'n_clicks')],
    [State('input-box', 'value')]
    )
def update_graph(no_clicked,input_value):
    if no_clicked is None:
         raise PreventUpdate
    elif input_value is None:
         raise PreventUpdate
    else:
        return dcc.Graph(
            id='indicator-graphic',
            figure={
                'data': [
                 {'x': [2, 1, 3, 4], 'y': [2, 3, 1, 4], 'type': 'line', 'name': 'stock'},
                ],
                'layout': {
                    'title': 'stock sentiment'
                }
            }
        )

if __name__ == "__main__":
    app.run_server(debug=True)