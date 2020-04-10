import json
import pymongo
import requests
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
import dash_html_components as html
import dash_bootstrap_components as dbc

from average_sent import Score
from sshtunnel import SSHTunnelForwarder

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

