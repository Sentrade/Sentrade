import json
import pymongo
import requests
import pandas as pd
import datetime as dt
from datetime import datetime
import dash_html_components as html
import dash_bootstrap_components as dbc

from average_sent import Score
from sshtunnel import SSHTunnelForwarder

def F_data(ticker):

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
        
        f_data = {}
        for record in stock_price_collection.find({"company_name":ticker, "date": "2019-09-16"}):
            f_data["open"] = record["open"]
            f_data["close"] = record["close"]
            f_data["high"] = record["high"]
            f_data["low"] = record["low"]
            f_data["volume"] = record["volume"]
        
        string = datetime.today().strftime("%b %d %Y")
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
                dbc.Row(html.H3(string, style={
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
                    dbc.Col(html.Div(Score(ticker)), width=5)
                ],
                )
                ],
                style={
                    'border-radius' : '5px',
                    'background-color': 'rgba(120,120,120,0.15)',
                    'width':'92.7%',
                    'margin-top':'5%',
                    'margin-left':'3.7%'
                }),
                
            ]
        )

        finance = html.Div(row)

        data = html.Div(finance)

    return data

