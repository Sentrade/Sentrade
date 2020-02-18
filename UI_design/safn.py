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
            className="dropdown",
            children=[
                dcc.Dropdown(
                    options=[
                        {'label': 'AAPL', 'value': 'AAPL'}],
                        value=['AAPL', 'AAPL'],
                        multi=False
                ),
            ], style={'width':'20%'}
        ),
        # Graph and news
        html.Div(
            className="two columns panel",
            children=[
                # Div for Graph
                html.Div(
                    [
                        dcc.Graph(id='graph-with-slider'),
                        dcc.Slider(
                            id='year-slider',
                            min=df['year'].min(),
                            max=df['year'].max(),
                            value=df['year'].min(),
                            marks={str(year): str(year) for year in df['year'].unique()},
                            step=None
                        )    
                    ], style={'width':'100%'}
                ),
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
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(dict(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'type': 'log', 'title': 'GDP Per Capita',
                   'range':[2.3, 4.8]},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},
        )
    }

if __name__ == "__main__":
    app.run_server(debug=True)