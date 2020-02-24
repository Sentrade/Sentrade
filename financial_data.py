import json
import pymongo
import requests
import pandas as pd
import datetime as dt
import dash_html_components as html

from sshtunnel import SSHTunnelForwarder

def F_data(ticker):

    db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
    db = db_client["sentrade_db"]

    if not ticker:
        data = html.H3(
            "No ticker selected.",
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
        
        string = ticker + " on SEPT 16"
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
        data = html.Div([
            html.Div([html.H3(string)]),
            html.Div([html.P(open_string)]),
            html.Div([html.P(close_string)]),
            html.Div([html.P(high_string)]),
            html.Div([html.P(low_string)]),
            html.Div([html.P(volume_string)]),
            ]
        )
    return data

