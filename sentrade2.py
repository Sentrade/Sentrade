#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Davide Locatelli"
__status__ = "prototype"

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pymongo
from sshtunnel import SSHTunnelForwarder
from plotly.subplots import make_subplots

app = dash.Dash(__name__,meta_tags=[{"name":"viewport", "content": "width=device-width"}])
server = app.server

db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
db = db_client["sentrade_db"]
stock_price_collection = db["stock_price"]
sentiment_collection = db["news"]

"""
close = []
stock_date = []
for record in stock_price_collection.find({"company_name":"AMZN"}):
    close.append(record["close"])
    stock_date.append(record["date"])

polarity = []
sent_date = []

for record in sentiment_collection.find():
    polarity.append(record["polarity"])
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

#for record in collection:
    #print(record["date"])

#fig = go.Figure()
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(eth_close,secondary_y=False)
fig.add_trace(eth_polarity,secondary_y=True)
fig.update_layout(
    margin= {'b': 0, 'r': 10, 'l': 60, 't': 0},                   
    legend= {'x': 0},
    xaxis=go.layout.XAxis(
        rangeslider=dict(
            visible=False
        ),
        rangeselector=dict(
            buttons=list([
                dict(
                    count=1,
                    label="1D",
                    step="day",
                    stepmode="backward"
                ),
                dict(
                    count=7,
                    label="1W",
                    step="day",
                    stepmode="backward"
                ),
                dict(
                    count=1,
                    label="1M",
                    step="month",
                    stepmode="backward"
                ),
                dict(
                    count=3,
                    label="3M",
                    step="month",
                    stepmode="backward"
                ),
                dict(
                    count=6,
                    label="6M",
                    step="month",
                    stepmode="backward"
                ),
                dict(
                    count=1,
                    label="1Y",
                    step="year",
                    stepmode="backward"
                ),
                dict(label='ALL',step="all")
            ]),
            font=dict(
                    family="Arial",
                    size=16,
                    color="white"
            ),
            bgcolor="#BABABA",
            activecolor='#949494',
            x=0.35,
            y=-0.13
        ),
        type="date"
    )
)
graph = dcc.Graph(figure=fig)

app.layout = html.Div(
    children = [
        graph
    ]
)
if __name__ == "__main__":
    app.run_server(debug=True)
"""
for record in stock_price_collection.find({"company_name":"AMZN"}):
    print(record["close"])