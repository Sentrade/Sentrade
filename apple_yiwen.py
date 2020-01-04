# Note: this can be setup in the requirments.txt
import yfinance as yf
import json
from pandas_datareader import data as pdr


# Input Information:
# First argument: stock name. eg. "AAPL" or "aapl", not case sensitive
# Second argument: customized start date
# Thrid argument: customized end data
def fetch_data(*args):
    yf.pdr_override()
    data = pdr.get_data_yahoo(args[0], args[1], args[2])

    return data


def historical_data(*args):
    data = fetch_data(*args)
    data['Date'] = data.index
    # modified data
    mod_data = data.drop(['Adj Close', 'Volume'], axis=1)
    json_data = mod_data.to_json(orient='records', date_format='iso')
    with open('./data/data.json', 'w') as outfile:
        json.dump(json_data, outfile)


historical_data("AAPL", "2015-01-01", "2020-01-02")
