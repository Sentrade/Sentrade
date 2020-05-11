#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from pymongo import MongoClient
from bson.json_util import dumps

__author__ = "Ziyou Zhang"
__status__ = "Production"

app = Flask(__name__)
app.config["DEBUG"] = False

client_address = "mongodb://admin:sentrade@45.76.133.175:27017"

@app.route('/data/apple', methods=['GET'])
def apple_data():
    client = MongoClient(client_address)
    db = client.sentiment_data["apple"]
    sentiment_data = db.find()
    data = []
    for sentiment in sentiment_data:
        data.append(sentiment)
    client.close()
    return dumps(data)

@app.route('/data/amazon', methods=['GET'])
def amazon_data():
    client = MongoClient(client_address)
    db = client.sentiment_data["amazon"]
    sentiment_data = db.find()
    data = []
    for sentiment in sentiment_data:
        data.append(sentiment)
    client.close()
    return dumps(data)

@app.route('/data/facebook', methods=['GET'])
def facebook_data():
    client = MongoClient(client_address)
    db = client.sentiment_data["facebook"]
    sentiment_data = db.find()
    data = []
    for sentiment in sentiment_data:
        data.append(sentiment)
    client.close()
    return dumps(data)

@app.route('/data/google', methods=['GET'])
def google_data():
    client = MongoClient(client_address)
    db = client.sentiment_data["google"]
    sentiment_data = db.find()
    data = []
    for sentiment in sentiment_data:
        data.append(sentiment)
    client.close()
    return dumps(data)

@app.route('/data/microsoft', methods=['GET'])
def microsoft_data():
    client = MongoClient(client_address)
    db = client.sentiment_data["microsoft"]
    sentiment_data = db.find()
    data = []
    for sentiment in sentiment_data:
        data.append(sentiment)
    client.close()
    return dumps(data)

@app.route('/data/netflix', methods=['GET'])
def netflix_data():
    client = MongoClient(client_address)
    db = client.sentiment_data["netflix"]
    sentiment_data = db.find()
    data = []
    for sentiment in sentiment_data:
        data.append(sentiment)
    client.close()
    return dumps(data)

@app.route('/data/tesla', methods=['GET'])
def tesla_data():
    client = MongoClient(client_address)
    db = client.sentiment_data["tesla"]
    sentiment_data = db.find()
    data = []
    for sentiment in sentiment_data:
        data.append(sentiment)
    client.close()
    return dumps(data)

@app.route('/data/uber', methods=['GET'])
def uber_data():
    client = MongoClient(client_address)
    db = client.sentiment_data["uber"]
    sentiment_data = db.find()
    data = []
    for sentiment in sentiment_data:
        data.append(sentiment)
    client.close()
    return dumps(data)

app.run(host='0.0.0.0', port=80)