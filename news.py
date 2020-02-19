#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import pandas as pd
import datetime as dt
import dash_html_components as html

__author__ = "Davide Locatelli"

def News(ticker):
    
    if not ticker:

        news = html.H3(
            "No ticker selected.",
            style={
                'margin-top':'0px',
                'textAlign':'center',
                'color':'#9C9C9C'
            }
        )

    else:
        companies = {
            "AMZN" : "amazon",
            "AAPL"  : "apple", 
            "FB"    : "facebook",
            "GOOG"  : "google",
            "MSFT"  : "microsoft",
            "NFLX"  : "netflix",
            "TSLA"  : "tesla",
            "UBER"  : "uber"
        }
        api_call = 'https://newsapi.org/v2/everything?q='
        api_call += companies[ticker]
        api_call += '&from=2020-01-20&sortBy=popularity&apiKey=954c05db19404ee99531875f66d9d138'
        response = requests.get(api_call)
        articles = response.json()["articles"]
        df = pd.DataFrame(articles)
        df = pd.DataFrame(df[["title","url"]])
        max_rows = 20

        news = html.Div(
            children = [
                html.P(
                    className = "p-news",
                    children = "Headlines"
                ),
                html.P(
                    className = "p-news-float-right",
                    children = "Last update: " + dt.datetime.now().strftime("%H:%M:%S") 
                ),
                html.Table(
                    className = "table-news",
                    children = [
                        html.Tr(
                            children = [
                                html.Td(
                                    children = [
                                        html.A(
                                            className = "td-link",
                                            children = df.iloc[i]["title"],
                                            href = df.iloc[i]["url"],
                                            target = "_blank",
                                        )
                                    ]
                                )
                            ]
                        )
                        for i in range(min(len(df),max_rows))
                    ] 
                )
            ]
        )

    return news
