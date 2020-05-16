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
from newsapi import NewsApiClient
from app.currentsentiment import get_score
from data.prediction_UI import get_prediction

from textwrap import dedent as d
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from plotly import tools
from datetime import datetime, timedelta

__author__ = "Davide Locatelli"
__status__ = "Production"

aboutus = """
With Sentrade you can explore the correlation between financial data and sentiment analysis.

Once a ticker is selected, you will see its recent financial data as well as a sentiment analysis score based on the latest news.
We use this sentiment score to predict the stock movement for the current day. To do this, we trained a machine learning model on historical Tweets. You can explore our historical data by clicking on the graph. You will be able to see the financial data, sentiment score and relevant tweets from the selected day.

This is a temporary website built by 6 MSc students from Imperial College London and it will be removed in June 2020. 
SenTrade makes no express or implied warranty that the website will be updated timely: please do not use it for trading purposes. SenTrade will not be liable for any damages or losses caused by the use of information provided.

If you are interested in the raw sentiment data to do your own analysis, call REST API via
http://api-sentrade.doc.ic.ac.uk/data/<company_name>
where company name can be chosen from: apple, amazon, facebook, google, microsoft, netflix, tesla, uber.
"""

easter_egg_message = """
‘三’百年前，将军前去战场，战事胶着，将军心急如焚，提脚
‘踹’向地面，忽见地面裂开一条细缝，金光闪烁，掘地一尺有余
‘得’宝剑一柄，后将军奋勇杀敌，所向披靡，战事得胜，将军获封为封疆大吏

后世人们为了纪念这个故事，将此事编为歌谣，传颂至今。歌名唤作‘三踹得’
"""


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

def Topbar(ticker):
    """
    Returns the topbar.

    :param ticker: string of the ticker
    :return topbar: hmtl.Div
    """

    if not ticker:
        return

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

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
    stock_price_db = db_client.stock_data
    records = stock_price_db[company_db_name[ticker]].find().sort([("$natural", -1)]).limit(1)
    for record in records:
        price = record['close']
        gain = price - record['open']
    gain_style = {
        'margin-left':'7px',
        'margin-top':'5px',
        'margin-right':'14px',
        'width':'auto'}
    if gain <= 0:
        gain = "{:.2f}".format(gain)
        gain_style['color'] = 'red'
    else:
        gain = "{:.2f}".format(gain)
        gain = "+" + gain
        gain_style['color'] = 'green'

    prediction_string, prediction_colour = Prediction(ticker)

    topbar = html.Div([
        html.H3(ticker,
        style={
            'font-family':'sans-serif',
            'font-weight':'700',
            'font-size':'2.3rem',
            'margin-top':'10px',
            'margin-left': '24.5px',
            'letter-spacing':'0.5px',
            'width':'auto'
        }),
        html.H6(companies[ticker],
        style={
            'margin-top':'33px',
            'margin-left':'10px',
            'color':'grey',
            'font-weight': '600',
            'width':'auto'
        }),
        html.Div([
            html.Div([
                html.P(price,
                style={
                    'font-family':'sans-serif',
                    'margin-top':'2px',
                    'font-size':'1.2em',
                    'font-weight': '900',
                    'width':'auto',
                    'color':'black',
                    'margin-bottom':'0'
                    }),
                html.P("At Close",
                style={
                    'font-family':'sans-serif',
                    'color':'#737373',
                    'font-size':'8pt',
                    'font-weight':'500',
                    'margin-top':'0',
                })
            ]),
            html.Div([
            html.P(gain,
                style=gain_style),
                ])],
            style={
                'display':'flex',
                'margin-top':'6px',
                'right':'460px',
                'position':'absolute',
                'border-right':'1px solid #e5e5e5',
                'height':'45px'
        }),
        html.Div([
            html.P(prediction_string,
            style={
                'font-family':'sans-serif',
                'font-weight':'500',
                'color':'#4F594F'
            }
            )],
        style={
            'height':'40px',
            'line-height':'40px',
            'margin-top':'9px',
            'right':'115px',
            'position':'absolute',
            'width':'200px',
            'text-align':'center',
            'border-radius':'5px',
            'background' : prediction_colour
        })
    ],
    style={
        'height': '60px',
        'border-bottom':'1px solid #e5e5e5',    
        'display':'flex'    
    })
    return topbar

instruction = html.H6(
    "Select a ticker",
    id= 'instruction'
)

def collect_stock_data(db,company,close,date):
    """
    Collects stock data from database and populates corresponding arrays with data.

    :param db: the database
    :param company: the company
    :param close: the array of close data that needs to be populated
    :param date: the array of dates that needs to be populated
    """

    for record in db[company].find().sort("date"):
        close.append(record["close"])
        date.append(record["date"])

def collect_sentiment_data(db,company,bert,blob,date):
    """
    Collects sentiment data from database and populates corresponding arrays with data.

    :param db: the database
    :param company: the company
    :param bert: the array of bert sentiment data that needs to be populated
    :param blob: the array of blob sentiment data that needs to be populated
    :param date: the array of dates that needs to be populated
    """

    for record in db[company].find({"7_day_sentiment_score":{"$exists":True}}).sort("date"):
        if record["7_day_sentiment_score"] != 0:
            blob.append(record["7_day_sentiment_score"])
            date.append(record["date"])

    for record in db[company].find({"7_day_bert_sentiment_score":{"$exists":True}}).sort("date"):
        if record["7_day_bert_sentiment_score"] != 0:
            bert.append(record["7_day_bert_sentiment_score"])

    for record in db[company].find({"sentiment_current":{"$exists":True}}).sort("date"):
        if record["sentiment_current"]:
            blob.append(record["sentiment_current"])
            date.append(record["date"])


def Graph(ticker):
    """
    Returns the graph figure.

    :param ticker: string of the ticker
    :return fig: plotly.graph_object figure
    """

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)

    if not ticker:

        ticker = "AAPL"

    stock_price_db = db_client.stock_data
    sentiment_db = db_client.sentiment_data

    close = []
    stock_date = []
    collect_stock_data(stock_price_db,company_db_name[ticker],close,stock_date)
    
    bert_polarity = []
    blob_polarity = []
    sent_date = []
    collect_sentiment_data(sentiment_db,company_db_name[ticker],bert_polarity,blob_polarity,sent_date)

    sentiment = []
    for i in range(len(bert_polarity)):
        bert = bert_polarity[i]
        bert *= 100
        bert_polarity[i] = bert
        blob = blob_polarity[i] + 1
        blob /= 2
        blob *= 100
        blob_polarity[i] = blob
        score = bert + blob
        score /= 2
        sentiment.append(score)

    records = stock_price_db[company_db_name[ticker]].find().sort([("$natural", -1)]).limit(1)
    for record in records:
        price = record['close']
        gain = price - record['open']
    stock_color = 'rgb(57,126,46)'
    if gain <= 0:
        stock_color = 'rgb(204,36,34)'
 
    eth_close = go.Scatter(
        y = close,
        x = stock_date,
        name= "Close",
        mode = "lines",
        line=dict(color=stock_color)
    )

    eth_polarity = go.Scatter(
        y = sentiment,
        x = sent_date,
        name = "Sentiment",
        mode = "lines",
        line=dict(color="rgba(111,192,245,0.8)")
    )

    fig = make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(eth_close,secondary_y=False)
    fig.add_trace(eth_polarity,secondary_y=True)
    fig.update_layout(
        margin= {'b': 0, 'r': 10, 'l': 60, 't': 0},                   
        legend= {'x': 0.35,'y':-0.1},
        xaxis=go.layout.XAxis(
            rangeslider=dict(
                visible=False
            ),
            range= ["2018-11-01","2019-09-30"],
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="     1D     ",
                        step="day",
                        stepmode="backward"),
                    dict(count=7,
                        label="     1W     ",
                        step="day",
                        stepmode="backward"),
                    dict(count=1,
                        label="    1M     ",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="     3M     ",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="     6M     ",
                        step="month",
                        stepmode="backward"
                        ),
                    dict(count=1,
                        label="     1Y     ",
                        step="year",
                        stepmode="backward"),
                    dict(label='     ALL     ',
                    step="all")
                ]),
                x=0.05,
                y=1.01,
                font=dict(
                    family="sans-serif",
                    size=15,
                    color="#828282"),
                bgcolor='#f5f5f5',
                activecolor='#dbdbdb'
            ),
            type="date"
        ),
        legend_orientation="h"
    )
    return fig

def Prediction(ticker):
    """
    Returns the prediction of the stock movement.

    :param ticker: string of the ticker
    :return prediction: the prediction
    :return colour: the colour the prediction needs to be displayed in
    """

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
    stock_price_db = db_client.stock_data
    records = stock_price_db[company_db_name[ticker]].find().sort([("$natural", -1)]).limit(1)
    for record in records:
        date = record["date"]

    prediction = get_prediction(company_db_name[ticker],date)

    if (prediction == -5):
        colour = "#f2f2f2"
        string = "Prediction not available"

    if (prediction == 0):
        colour = "#f2f2f2"
        string = "Stable"

    if (prediction == 1):
        colour = "rgba(3, 164, 3, 0.5)"
        string = "Rise up to 5%"

    if (prediction == 2):
        colour = "rgba(3, 164, 3, 0.5)"
        string = "Rise over 5%"

    if (prediction == -1):
        colour = "rgba(164, 19, 3,0.5)"
        string = "Fall up to 5%"

    if (prediction == -2):
        colour = "rgba(164, 19, 3,0.5)"
        string = "Fall over 5%"

    return string, colour

def Tweets(ticker, graphDate,default=False):
    """
    Returns the tweets section.

    :param ticker: string of the ticker
    :param graphDate: the date of the tweets
    :param default: default flag, True if section is in default
    :return news: html.Div
    """

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

        if default:
            api = NewsApiClient(api_key='954c05db19404ee99531875f66d9d138')
            three_days_ago = datetime.strptime(graphDate,'%Y-%m-%d') - timedelta(days=3)
            all_articles = api.get_everything(q=company_db_name[ticker],
                                    sources='bloomberg,business-insider,financial-post,fortune,recode,reuters,techcrunch,techradar,the-verge',
                                    from_param=three_days_ago,
                                    to=graphDate,
                                    language='en',
                                    sort_by='relevancy',
                                    page=2)
            articles = []
            links = []
            for article in all_articles["articles"]:
                articles.append(article["title"])
                links.append(article["url"])

            scores = []
            for title in articles:
                scores.append(get_score(title))

            news = html.Div(
                children = [
                    html.Div(
                        html.Img(src='assets/news-logo.png',
                            style={'height':'50px',
                                'margin-left':'30%'})),
                    html.Div(
                        className = "table-news",
                        children = [
                            html.Div(
                                children = [
                                    html.Div(
                                        children = [
                                            html.A(
                                                className = "td-link",
                                                children = articles[i],
                                                href = links[i],
                                                target = "_blank",
                                            )
                                        ],
                                        style={
                                            'height':'auto',
                                            'width':'auto',
                                            'font-size' : '0.8rem',
                                            'font-family' : 'sans-serif',
                                            'margin-left':'10px',
                                            'margin-right':'10px',
                                            'line-height':'20px'
                                        }
                                    )
                                ],
                                style=tweetstyle(scores,i,True)
                            )
                            for i in range(len(articles))
                        ],
                        style={
                            'margin-left' :'3%',
                            'margin-right': '3%',
                            'margin-bottom': '3%'
                        }
                    )
                ],
                style={
                    'background-color':'#f2f2f2',
                    'border-radius':'5px',
                    'margin-right' : '5.5%',
                    'overflow':'scroll',
                    'display':'block',
                    'margin-top' : '2%',
                    'height':'570px'
                }
            )
            return news
            
        
        db = db_client.twitter_data[company_db_name[ticker]]
        dates = db.distinct("date")
        
        if graphDate in dates:

            tweets = []
            tweets_polarity = []
            for record in db.aggregate([
                { "$match" : {"date" : graphDate}},
                { "$sample" : {"size" : 100 } }
                ]):
                if record["original_text"] not in tweets:
                    tweets.append(record["original_text"])
                    tweets_polarity.append(record["polarity"])

        else:
            tweets = ["No Tweets."]
            tweets_polarity = ["None"] 
            
        news = html.Div(
            children = [
                html.Div(
                    html.Img(src='./assets/Twitter_Logo_Blue.png',
                        style={'height':'50px',
                            'margin-left':'43%'})),
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
                                        'height':'auto',
                                        'width':'auto',
                                        'font-size' : '0.8rem',
                                        'font-family' : 'sans-serif',
                                        'margin-left':'10px',
                                        'margin-right':'10px',
                                        'line-height':'20px'
                                    }
                                )
                            ],
                            style=tweetstyle(tweets_polarity,i)
                        )
                        for i in range(len(tweets))
                    ],
                    style={
                        'margin-left' :'3%',
                        'margin-right': '3%',
                        'margin-bottom': '3%'
                    }
                )
            ],
            style={
                'background-color':'#f2f2f2',
                'border-radius':'5px',
                'margin-right' : '5.5%',
                'overflow':'scroll',
                'display':'block',
                'margin-top' : '2%',
                'height':'570px'
            }
        )

        return news

def tweetstyle(tweets_polarity, i,default=False):
    """
    Determines the colour of a tweet based on its polarity.

    :param tweets_polarity: the array of polarities
    :param i: the position of the tweet polarity in the array
    :param default: default flag, True if section is in default
    :return style: dict
    """
    
    if default:
        style = {
            'background-color' : 'rgba(250, 192, 0,0.5)',
            'border-radius' : '5px',
            'margin-top':'1%'
        }
        if tweets_polarity[i] < 33:
            style = {
                'background-color' : 'rgba(164, 19, 3,0.5)',
                'border-radius' : '5px',
                'margin-top' : '1%'
            }
        if tweets_polarity[i] > 66:
            style = {
                'background-color' : 'rgba(3, 164, 3, 0.5)',
                'border-radius' : '5px',
                'margin-top' : '1%'
            }
        return style

    if tweets_polarity[i] == "None":
        style = {
            'background-color' : 'white',
            'border-radius' : '5px',
            'margin-top' : '1%'
        }
        return style

    style = {
        'background-color' : 'rgba(250, 192, 0,0.5)',
        'border-radius' : '5px',
        'margin-top':'1%'
    }

    if tweets_polarity[i] < -0.3:
        style = {
            'background-color' : 'rgba(164, 19, 3,0.5)',
            'border-radius' : '5px',
            'margin-top' : '1%'
        }
        
    if tweets_polarity[i] > 0.3:
        style = {
            'background-color' : 'rgba(3, 164, 3, 0.5)',
            'border-radius' : '5px',
            'margin-top' : '1%'
        }
    return style

def F_data(ticker, graphDate, default=False):
    """
    Returns the financial data section.

    :param ticker: string of the ticker
    :param graphDate: the date of the data
    :param default: the default flag, True if section is in default
    :return data: html.Div
    """

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
    db = db_client.stock_data

    if not ticker:

        ticker = "AAPL"

    stock_price_collection = db[company_db_name[ticker]]

    dateString = datetime.strptime(graphDate, "%Y-%m-%d")
    dateString = dateString.strftime("%b %d %Y")

    dateString = html.P(dateString, style={
                    'font-family':'sans-serif',
                    'font-weight':'500',
                    'letter-spacing':'1px',
                    'font-size':'10pt',
                    'textAlign':'center',
                    'color':'#737373',
                    'left':'40px',
                    'position':'absolute',
                    'margin-top': '2%'
                })


    f_data = {}

    for record in stock_price_collection.find({"date": graphDate}):
        f_data["open"] = record["open"]
        f_data["close"] = record["close"]
        f_data["high"] = record["high"]
        f_data["low"] = record["low"]
        f_data["volume"] = record["volume"]
        f_data["change"] = record["change"]
    
    if (f_data):
        magnitude = 0
        vol = f_data["volume"]
        while abs(vol) >= 1000:
            magnitude += 1
            vol /= 1000.0
        volume_string = '%.2f%s' %(vol, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])
        change_string = '%.2f'%(f_data["change"])
        open_string = str(f_data["open"])
        close_string = str(f_data["close"])
        high_string = str(f_data["high"]) 
        low_string = str(f_data["low"])
    else:
        volume_string = "--"
        change_string = "--"
        open_string = "--"
        close_string = "--"
        high_string = "--"
        low_string = "--"
    
    row = html.Div([
        dateString,
        html.Div([
            html.Div([
                html.Div([
                    html.P("Open",
                    style={
                        'font-family':'sans-serif',
                        'color':'#737373',
                        'font-size':'8pt',
                        'font-weight':'500',
                        'margin-top':'0',
                        }),
                    html.P("Close",
                    style={
                        'font-family':'sans-serif',
                        'color':'#737373',
                        'font-size':'8pt',
                        'font-weight':'500',
                        'margin-top':'0',
                    })
                ]),
                html.Div([
                html.P(open_string,
                    style={'font-family':'sans-serif',
                        'color':'#383838',
                        'font-size':'8pt',
                        'font-weight':'700',
                        'margin-left':'40px',
                        'margin-top':'0',}),
                html.P(close_string,
                    style={'font-family':'sans-serif',
                        'color':'#383838',
                        'font-size':'8pt',
                        'font-weight':'700',
                        'margin-left':'40px',
                        'margin-top':'0',})
                    ])],
                style={
                    'display':'flex',
                    'margin-top':'2px',
                    'left':'40px',
                    'top':'500px',
                    'position':'absolute',
                    'border-right':'1px solid #e5e5e5',
                    'height':'45px',
                    'width' : '130px'
            }),
            html.Div([
            html.Div([
                html.P("High",
                style={
                    'font-family':'sans-serif',
                    'color':'#737373',
                    'font-size':'8pt',
                    'font-weight':'500',
                    'margin-top':'0',
                    }),
                html.P("Low",
                style={
                    'font-family':'sans-serif',
                    'color':'#737373',
                    'font-size':'8pt',
                    'font-weight':'500',
                    'margin-top':'0',
                })
            ]),
            html.Div([
            html.P(high_string,
                style={'font-family':'sans-serif',
                    'color':'#383838',
                    'font-size':'8pt',
                    'font-weight':'700',
                    'margin-left':'40px',
                    'margin-top':'0',}),
            html.P(low_string,
                style={'font-family':'sans-serif',
                    'color':'#383838',
                    'font-size':'8pt',
                    'font-weight':'700',
                    'margin-left':'40px',
                    'margin-top':'0',})
                ])
                ],
            style={
                'display':'flex',
                'margin-top':'2px',
                'left':'190px',
                'top':'500px',
                'position':'absolute',
                'border-right':'1px solid #e5e5e5',
                'height':'45px',
                'width' : '124px'
        }),
        html.Div([
            html.Div([
                html.P("Vol",
                style={
                    'font-family':'sans-serif',
                    'color':'#737373',
                    'font-size':'8pt',
                    'font-weight':'500',
                    'margin-top':'0',
                    }),
                html.P("Change",
                style={
                    'font-family':'sans-serif',
                    'color':'#737373',
                    'font-size':'8pt',
                    'font-weight':'500',
                    'margin-top':'0',
                })
            ]),
            html.Div([
            html.P(volume_string,
                style={'font-family':'sans-serif',
                    'color':'#383838',
                    'font-size':'8pt',
                    'font-weight':'700',
                    'margin-left':'40px',
                    'margin-top':'0',}),
            html.P(change_string,
                style={'font-family':'sans-serif',
                    'color':'#383838',
                    'font-size':'8pt',
                    'font-weight':'700',
                    'margin-left':'40px',
                    'margin-top':'0',})
                ])
                ],
            style={
                'display':'flex',
                'margin-top':'2px',
                'left':'334px',
                'top':'500px',
                'position':'absolute',
                'border-right':'1px solid #e5e5e5',
                'height':'45px',
                'width' : '145px'
        }),
        html.Div([
            html.P("Sentiment",
                style={
                    'font-family':'sans-serif',
                    'color':'#737373',
                    'font-size':'8pt',
                    'font-weight':'500',
                    'margin-top':'15px'
                    }),
            html.Div(Score(ticker,graphDate,default),
            style={
                'margin-top':'15px',
                'margin-left':'40px'
            })],
        style={
            'margin-top':'2px',
            'left':'499px',
            'top':'500px',
            'position':'absolute',
            'border-right':'1px solid #e5e5e5',
            'height':'45px',
            'width' : '336px',
            'display':'flex'
        })
        ],style={'display':'flex'})
    ])

    finance = html.Div(row)

    data = html.Div(finance)

    return data

def Score(ticker, graphDate, default=False):
    """
    Returns the score progress bar.

    :param ticker: string of the ticker
    :param graphDate: the date of the score
    :param default: default flag, True if section is in default
    :return polarity: html.Div
    """
    
    if default:
        api = NewsApiClient(api_key='954c05db19404ee99531875f66d9d138')
        three_days_ago = datetime.strptime(graphDate,'%Y-%m-%d') - timedelta(days=3)
        all_articles = api.get_everything(q=company_db_name[ticker],
                                sources='bloomberg,business-insider,financial-post,fortune,recode,reuters,techcrunch,techradar,the-verge',
                                from_param=three_days_ago,
                                to=graphDate,
                                language='en',
                                sort_by='relevancy',
                                page=2)
        articles = []
        for article in all_articles["articles"]:
            articles.append(article["title"])

        scores = []
        for title in articles:
            scores.append(get_score(title))
            
        score = sum(scores)/len(scores)
        polarity_value_string = "{:.0f}%".format(score)
        polarity = html.Div([
                html.Div(dbc.Progress(polarity_value_string, value=score, color=score_style(score),className="mb-3")),
                ],
                style={'width':'200px',
                'border-radius':'5px'}
            )
        return polarity

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)

    if not ticker:

        ticker = "AAPL"

    else:
        
        db = db_client.sentiment_data[company_db_name[ticker]]
        dates = db.distinct("date")
        if graphDate in dates:
            scores = {}
            for record in db.find({"date": graphDate}):
                bert = record["7_day_bert_sentiment_score"]
                blob = record["7_day_sentiment_score"] + 1
                bert *= 100
                blob /= 2
                blob *= 100
                score = bert + blob
                score /= 2
                scores[graphDate] = score

            polarity_value = scores[graphDate]

            polarity_value_string = "{:.0f}%".format(polarity_value) 
            polarity = html.Div([
                html.Div(dbc.Progress(polarity_value_string, value=polarity_value, color=score_style(polarity_value),className="mb-3")),
                ],
                style={'width':'200px',
                'border-radius':'5px'}
            )
        else:
            polarity = html.Div([
                html.Div("--"),
                ]
            )

    return polarity

def score_style(polarity_value):
    """
    Returns colour of score progress bar based on polarity score.

    :param polarity_value: the polarity
    :return color: the colour of the progress bar
    """
    color = 'warning'
    if polarity_value < 33:
        color = 'danger'
    if polarity_value > 66:
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
                    dbc.Col(dbc.NavbarBrand("Sentrade", className="ml-2", href='http://sentrade.doc.ic.ac.uk/')),
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
    children= dcc.Graph(id='click-graph', config={'editable':False,'displaylogo':False,'displayModeBar':True,'modeBarButtonsToRemove':['toImage','zoom2d','pan2d','resetScale2d','hoverCompareCartesian','hoverClosestCartesian','toggleSpikelines']})
)



data = html.Div(
    className= 'finance',
    id = 'finance'
)

topbar = html.Div(
    className= 'topbar',
    id = 'topbar'
)

question = html.Div([

         html.P(
              "?",
              id="tooltip-target",
              style={
                     "textAlign": "center", 
                     "color": "white",
                     "position":"absolute",
                     "left":'540px',
                     "font-size":"8pt",
                     "top":'425px',
                     "background-color":"#cfcfcf",
                     "border-radius":"50%",
                     "width":"15px",
                     "height":"15px",
                     "line-height":"15px",
                     "cursor":"pointer",
                     "margin-left":"1px",
                     "margin-right":"1px"
              },
              className="dot"),

         dbc.Tooltip(
              "The sentiment score is the average of the Google BERT and TextBlob scores of the tweets about the selected ticker over a time period of seven days.",
               target="tooltip-target",
         )
    ],
    id = 'question')

leftdiv = html.Div(
    [
        graph,
        question,
        data
    ]
)

tweets = html.Div(
    className = 'tweets',
    id = 'tweets',
)

contents = html.Div(
    className= 'contents',
    children= html.Div([
        topbar,
        instruction,
        dbc.Row([
            dbc.Col(leftdiv,width=8),
            dbc.Col(tweets)
        ])
    ])
)

def MainPage():
    """
    Returns the main page layout

    :return layout: html.Div
    """
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
    dash.dependencies.Output('click-graph','figure'),
    [dash.dependencies.Input('stock-ticker', 'value')])
def update_graph(ticker):
    return Graph(ticker)

@app.callback(
    [dash.dependencies.Output('click-graph','style'),
    dash.dependencies.Output('question','style')],
    [dash.dependencies.Input('stock-ticker', 'value')])
def show_graph(ticker):
    """
    Displays the graph based on ticker

    :param ticker: the ticker
    :return: two dicts setting visibility of graph and sentiment information
    """
    if not ticker:
        return {
            'display':'none'
        },{'display':'none'}
    else:
        return {
            'display':'block',
            'height':'450px'
        },{'display':'block'}

@app.callback(
    dash.dependencies.Output('instruction','style'),
    [dash.dependencies.Input('stock-ticker', 'value')])
def show_instruction(ticker):
    """
    Displays initial instruction based on ticker insertion

    :param ticker: the inserted ticker
    :return: dict setting visibility of instruction
    """
    if not ticker:
        return {
            'margin-top':'25%',
            'textAlign':'center',
            'color':'#9C9C9C',
            'display':'block'
        }
    return {
        'display':'none'
    }

@app.callback(
    dash.dependencies.Output('topbar','children'),
    [dash.dependencies.Input('stock-ticker', 'value')])
def update_topbar(ticker):
    """
    Updates the topbar according to the ticker selected

    :param ticker: the selected ticker
    :return Topbar: html.Div
    """
    return Topbar(ticker)

@app.callback(
    [dash.dependencies.Output('finance','children'),
    dash.dependencies.Output('tweets','children')],
    [dash.dependencies.Input('click-graph', 'clickData')],
    [dash.dependencies.State('stock-ticker', 'value')])
def update_finance_and_tweets(clickData,ticker):
    """
    Displays the tweets and finance sections according to clickData and ticker insertion

    :param clickData: data of clicks on the graph
    :param ticker: the ticker inserted
    :return F_data,Tweets: two html.Div
    """
    if not ticker:
        return html.Div(""),html.Div("")
    if clickData:
        graphDate = clickData["points"][0]["x"]
        return F_data(ticker,graphDate),Tweets(ticker,graphDate)
    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
    stock_price_db = db_client.stock_data
    for record in stock_price_db[company_db_name[ticker]].find().sort([("$natural", -1)]).limit(1):
        graphDate = record["date"]
    return F_data(ticker,graphDate,True),Tweets(ticker,graphDate,True)

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    """
    Controls the state of the navbar collapse

    :param n: number of clicks on collapse
    :param is_open: open state
    :return is_open: open/close state
    """
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
    """
    Controls the state of the modal collapse

    :param n1: number of clicks on modal
    :param n2: number of clicks on close button
    :param is_open: open state
    :return is_open: open/close state
    """
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    [Output('finance', 'style'),
    Output('tweets','style')],
    [Input('stock-ticker','value')])
def hide_finance_and_tweets(input):
    """
    Controls the visbility of the finance and tweets sections

    :param input: the ticker selection
    :return: two dicts setting the visibility
    """
    if input:
        return {'display':'block'},{'display':'block'}
    else:
        return {'display':'none'},{'display':'none'}

@app.callback(
    Output("click-graph", "clickData"), 
    [Input("stock-ticker", "value")]
)
def reset_clickData(n):
    """
    Resets the click data when new ticker is inserted

    :param n: new ticker inserted
    :return: None
    """
    if n is None:
        pass
    else:
        return None

# Debugging
if __name__ == "__main__":
    app.title = "SenTrade"
    app.run_server(debug=False, host='0.0.0.0', port=80)
