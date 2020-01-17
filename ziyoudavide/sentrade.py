#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#EEEDFA',
}

app.layout = html.Div(style={'backgroundColor':colors['background']}, children=[
    html.H1(
        children='SenTrade',
        style={
            'textAlign':'center'
        }
    ),

    html.Div(
        children='A web app to analyse the sentiment of the stock market.',
        style={
            'textAlign':'center'
        }
    ),

    html.Label('Ticker'),
    dcc.Dropdown(
        options=[
            {'label':'AAPL','value':'AAPL'},
            {'label':'DIS','value':'DIS'},
            {'label':'TSLA','value':'TSLA'}
        ],
        value='APPL'
    ),

    dcc.Slider(
        min = 1,
        max = 9,
        step=None,
        marks = {
            1: '1D',
            2: '1W',
            3: '1M',
            4: '3M',
            5: '6M',
            6: '1Y',
            7: '2Y',
            8: '5Y',
            9: '10Y'
        },
        value = 1,
    ),

    html.Label('Display'),
    dcc.Checklist(
        options=[
            {'label':'Stock','value':'ST'},
            {'label':'Sentiment','value':'SENT'}
        ],
        value = ['ST']
    ),

    dcc.Graph(
        id='stock-sentiment',
        figure={
            'data':[
                {'x':[1,2,3],'y':[4,1,2],'type':'bar','name':'SF'},
                {'x':[1,2,3],'y':[2,4,5],'type':'bar','name':'Montréal'},
            ],
            'layout':{
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background']
            }
        }
    )
])

if __name__=='__main__':
    app.run_server(debug=True)