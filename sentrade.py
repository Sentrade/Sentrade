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
from datetime import datetime, timedelta

__author__ = "Davide Locatelli"
__status__ = "Prototype"

aboutus = """
This website aims to provide sentiment analysis of eight stocks by applying natural language processing on Twitter posts. 

This is a temporary website built by 6 MSc students from Imperial College London and it will be removed in June 2020. 

SenTrade makes no express or implied warranty that the website will be updated timely: please do not use it for trading purposes. 

SenTrade will not be liable for any damages or losses caused by the use of information provided.

"""

easter_egg_message = """
‘三’百年前，将军前去战场，战事胶着，将军心急如焚，提脚
‘踹’向地面，忽见地面裂开一条细缝，金光闪烁，掘地一尺有余
‘得’宝剑一柄，后将军奋勇杀敌，所向披靡，战事得胜，将军获封为封疆大吏

后世人们为了纪念这个故事，将此事编为歌谣，传颂至今。歌名唤作‘三踹得’
"""

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
            "Select a ticker",
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
        sentiment_db = db_client.sentiment_data

        close = []
        stock_date = []
        for record in stock_price_db.find({"company_name":ticker}):
            close.append(record["close"])
            stock_date.append(record["date"])
        
        polarity = []
        sent_date = []
        for record in sentiment_db[company_db_name[ticker]].find().sort("date"):
            polarity.append(record["1_day_sentiment_score"])
            sent_date.append(record["date"])
        
        eth_close = go.Scatter(
            y = close,
            x = stock_date,
            name = "Close",
            mode = "lines",
            line=dict(color="#7a90e0")
        )

        eth_polarity = go.Scatter(
            y = polarity,
            x = sent_date,
            name = "Sentiment",
            mode = "lines",
            line=dict(color="#FFC300")
        )

        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(eth_close,secondary_y=False)
        fig.add_trace(eth_polarity,secondary_y=True)
        fig.update_layout(
            margin= {'b': 0, 'r': 10, 'l': 60, 't': 0},                   
            legend= {'x': 0},
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

def Prediction(ticker):

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
    db = db_client["sentrade_db"]

    if not ticker:
        pred = html.H3(
            "",
            style={
                'margin-top':'0px',
                'textAlign':'center',
                'color':'#9C9C9C'
            }
        )
    else:
        string = "expected "
        if ticker == "AAPL":
            string += "growth"
            color = "success"
        else:
            string += "drop"
            color = "danger"
        pred = dbc.Badge(string, color=color, style = {'width':'75%','height':'70%', 'border-radius':'5px'})

    return pred

def Tweets(ticker, graphDate):

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
    
    if not ticker:

        news = html.H3(
            "",
            style={
                'margin-top':'0px',
                'textAlign':'center',
                'color':'#9C9C9C'
            }
        )

    else:
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
        
        db = db_client.twitter_data[company_db_name[ticker]]
        dates = db.distinct("date")
        
        if graphDate in dates:

            tweets = []
            tweets_polarity = []
            for record in db.aggregate([
                { "$match" : {"date" : graphDate}},
                { "$sample" : {"size" : 10 } }
                ]):
                tweets.append(record["original_text"])
                tweets_polarity.append(record["polarity"])

            news = html.Div(
                children = [
                    html.H3(
                        className = "p-news",
                        children = "Tweets",
                        style={
                            'font-family':'sans-serif',
                            'font-weight':'500',
                            'letter-spacing':'1.5px',
                            'font-size':'1.1rem',
                            'textAlign':'left',
                            'color':'black',
                            'position':'relative',
                            'margin-top':'1.2%',
                            'margin-left' : '1%'
                        }
                    ),
                    html.Div(
                        className = "table-news",
                        children = [
                            html.Div(
                                children = [
                                    html.Div(
                                        children = [
                                            html.A(
                                                className = "td-link",
                                                children = tweets[i],
                                                target = "_blank",
                                            )
                                        ],
                                        style={
                                            'font-size' : '0.8rem',
                                            'font-family' : 'sans-serif'
                                        }
                                    )
                                ],
                                style=tweetstyle(tweets_polarity,i)
                            )
                            for i in range(len(tweets))
                        ],
                        style={
                            'margin-left' :'1%',
                            'margin-right': '1%',
                            'margin-bottom': '1%'
                        }
                    )
                ],
                style={
                    'background-color': 'rgba(120,120,120,0.15)',
                    'border-radius':'5px',
                    'margin-right' : '5.5%',
                    'overflow':'scroll',
                    'display':'block',
                    'margin-top' : '1.3%',
                    'height':'597px'
                }
            )

        else:

            news = html.Div(
                children = [
                    html.H3(
                        className = "p-news",
                        children = "Tweets",
                        style={
                            'font-family':'sans-serif',
                            'font-weight':'500',
                            'letter-spacing':'1.5px',
                            'font-size':'1.1rem',
                            'textAlign':'left',
                            'color':'black',
                            'position':'relative',
                            'margin-top':'1.2%',
                            'margin-left' : '1%'
                        }
                    ),
                    html.Div(
                        className = "table-news",
                        children = ["No twitter data for this day"],
                        style={
                            'margin-left' :'1%',
                            'margin-right': '1%',
                            'margin-bottom': '1%'
                        }
                    )
                ],
                style={
                    'background-color': 'rgba(120,120,120,0.15)',
                    'border-radius':'5px',
                    'margin-right' : '5.5%',
                    'overflow':'scroll',
                    'display':'block',
                    'margin-top' : '1.3%',
                    'height':'597px'
                }
            )

        return news

def tweetstyle(tweets_polarity, i):
    style = {
        'background-color' : 'rgba(235,158,62,0.5)',
        'border-radius' : '5px',
        'margin-top':'1%'
        }
    if tweets_polarity[i] < -0.3:
        style = {
            'background-color' : 'rgba(233,82,82,0.5)',
            'border-radius' : '5px',
            'margin-top' : '1%'
        }
    if tweets_polarity[i] > 0.3:
        style = {
            'background-color' : 'rgba(9,168,17,0.5)',
            'border-radius' : '5px',
            'margin-top' : '1%'
        }
    return style

def F_data(ticker, graphDate="2019-09-30"):

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
    db = db_client["sentrade_db"]

    if not ticker:

        data = html.H3(
            "",
            style={
                'margin-top':'0px',
                'textAlign':'center',
                'color':'#9C9C9C'
            }
        )
    else:

        stock_price_collection = db["stock_price"]
        dates = stock_price_collection.distinct("date")

        dateString = datetime.strptime(graphDate, "%Y-%m-%d")
        dateString = dateString.strftime("%b %d %Y")

        if graphDate in dates:

            f_data = {}

            for record in stock_price_collection.find({"company_name":ticker, "date": graphDate}):
                f_data["open"] = record["open"]
                f_data["close"] = record["close"]
                f_data["high"] = record["high"]
                f_data["low"] = record["low"]
                f_data["volume"] = record["volume"]
            
        
            open_string = "Open: " 
            open_string += str(f_data["open"])
            close_string = "Close: " 
            close_string += str(f_data["close"])
            high_string = "High: " 
            high_string += str(f_data["high"])
            low_string = "Low: " 
            low_string += str(f_data["low"])
            volume_string = "Volume: " 
            volume_string += str(f_data["volume"])
            row = html.Div(
                [
                    dbc.Row(html.H3(dateString, style={
                        'font-family':'sans-serif',
                        'font-weight':'500',
                        'letter-spacing':'1.5px',
                        'font-size':'1.1rem',
                        'textAlign':'center',
                        'color':'black',
                        'position':'absolute',
                        'margin-left': '5.2%',
                        'margin-top': '2%'
                    })),
                    html.Div([
                    dbc.Row(
                    [
                        dbc.Col(html.Div(open_string,style={'font-family':'sans-serif'}), width=3),
                        dbc.Col(html.Div(high_string,style={'font-family':'sans-serif'}), width=3),
                        dbc.Col(html.Div("Sentiment:",style={'font-family':'sans-serif'}), width=4)
                    ],
                    style={
                        'margin-top': '2%',
                    }
                    ),
                    dbc.Row(
                    [
                        dbc.Col(html.Div(close_string,style={'font-family':'sans-serif'}), width=3),
                        dbc.Col(html.Div(low_string,style={'font-family':'sans-serif'}), width=3),
                        dbc.Col(html.Div(Score(ticker, graphDate)), width=5)
                    ],
                    )
                    ],
                    style={
                        'border-radius' : '5px',
                        'background-color': 'rgba(120,120,120,0.15)',
                        'width':'91.3%',
                        'margin-top':'5.5%',
                        'margin-left':'3.7%'
                    }),
                    
                ]
            )

            finance = html.Div(row)

            data = html.Div(finance)

        else:
            row = html.Div(
                [
                    dbc.Row(html.H3(dateString, style={
                        'font-family':'sans-serif',
                        'font-weight':'500',
                        'letter-spacing':'1.5px',
                        'font-size':'1.1rem',
                        'textAlign':'center',
                        'color':'black',
                        'position':'absolute',
                        'margin-left': '5.2%',
                        'margin-top': '2%'
                    })),
                    html.Div([
                    dbc.Row(
                    [
                        dbc.Col(html.Div("No financial data for this day.",style={'font-family':'sans-serif'}), width=5),
                        dbc.Col(html.Div("Sentiment:",style={'font-family':'sans-serif'}), width=4)
                    ],
                    style={
                        'margin-top': '2%',
                    }
                    ),
                    dbc.Row(
                    [
                        dbc.Col(html.Div("",style={'font-family':'sans-serif'}), width=5),
                        dbc.Col(html.Div(Score(ticker, graphDate)), width=5)
                    ],
                    )
                    ],
                    style={
                        'border-radius' : '5px',
                        'background-color': 'rgba(120,120,120,0.15)',
                        'width':'91.3%',
                        'margin-top':'5.5%',
                        'margin-left':'3.7%'
                    }),
                    
                ]
            )

            finance = html.Div(row)

            data = html.Div(finance)


    return data

def Score(ticker, graphDate):

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)

    if not ticker:

        polarity = html.H3(
            "",
            style={
                'margin-top':'0px',
                'textAlign':'center',
                'color':'#9C9C9C'
            }
        )

    else:
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
        
        db = db_client.sentiment_data[company_db_name[ticker]]
        dates = db.distinct("date")
        if graphDate in dates:
            scores = {}
            for record in db.find({"date": graphDate}):
                scores[graphDate] = record["1_day_sentiment_score"]

            polarity_value = scores[graphDate] + 1
            polarity_value /= 2
            polarity_value *= 100

            polarity_value_string = "{:.0f}%".format(polarity_value) 
            polarity = html.Div([
                html.Div(dbc.Progress(polarity_value_string, value=polarity_value, color=score_style(scores[graphDate]),className="mb-3")),
                ]
            )
        else:
            polarity = html.Div([
                html.Div("No sentiment data for this day"),
                ]
            )

    return polarity

def score_style(polarity_avg):
    color = 'warning'
    if polarity_avg < -0.3:
        color = 'danger'
    if polarity_avg > 0.3:
        color = 'success'
    return color

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

graph = html.Div(
    className = 'graph',
    id = 'graph',
    style={
        'margin-top':'0.8%',
    },
    children= dcc.Graph(id='click-graph')
)

alert = html.Div(
    [
        dbc.Alert(
            "Click on points on the graph",
            id="alert-auto",
            is_open=True,
            dismissable=True,
            #duration=15000,
            style= {
                'width':'50%','margin-left':'auto','margin-right':'auto','border-radius':'5px','margin-top':'2%'
            }
        ),
    ]
)

data = html.Div(
    className= 'finance',
    children = [
        html.Div(
            id = 'instruction',
            children = alert
        ),
        html.Div(
            id = 'finance')
    ]
)

leftdiv = html.Div(
    [
        graph,
        data
    ]
)

tweets = html.Div(
    className = 'tweets',
    id = 'tweets',
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
    [dash.dependencies.Input('click-graph', 'clickData')],
    [dash.dependencies.State('stock-ticker', 'value')])
def update_tweets(clickData,ticker):
    graphDate = "2019-09-30"
    if clickData:
        graphDate = clickData["points"][0]["x"]
    return Tweets(ticker,graphDate)

@app.callback(
    dash.dependencies.Output('graph','children'),
    [dash.dependencies.Input('stock-ticker', 'value')])
def update_graph(ticker):
    #print("im trying to display a graph")
    return Graph(ticker)

@app.callback(
    [dash.dependencies.Output('finance','children'),
    dash.dependencies.Output('instruction','style')],
    [dash.dependencies.Input('click-graph', 'clickData')],
    [dash.dependencies.State('stock-ticker', 'value')])
def update_finance(clickData,ticker):
    if not ticker:
        return html.Div(""),{'display':'none'}
    if clickData:
        graphDate = clickData["points"][0]["x"]
    return F_data(ticker,graphDate),{'display':'none'}

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

@app.callback(
    [Output('finance', 'style'),
    Output('tweets','style')],
    [Input('stock-ticker','value')])
def hide_finance(input):
    if input:
        return {'display':'block'},{'display':'block'}
    else:
        return {'display':'none'},{'display':'none'}

@app.callback(
    Output("alert-auto", "is_open"),
    [Input("stock-ticker", "value")],
    [State("alert-auto", "is_open")],
)
def toggle_alert(ticker, is_open):
    if ticker != "None":
        return not is_open
    return is_open

# Debugging
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=80)
