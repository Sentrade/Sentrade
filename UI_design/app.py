#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stock_price_scrap_nora
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


colors = {
    'background': '#111111',
    'text': '#1b41c4'
}

app.layout = html.Div([
   

    html.Label('Stock ticker ',style={
            'textAlign': 'center',
            'color': colors['text']
        }),
    dcc.Input(id='input-box', value='AAPL', type='text'),
    html.Button('Submit', id='button'),

    dcc.Graph(id='indicator-graphic'),

    html.Div(id='output-container-button',
             children='Enter a value and press submit')

    
])
  
@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )

if __name__ == '__main__':
    app.run_server(debug=True)