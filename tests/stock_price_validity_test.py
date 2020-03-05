#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from pymongo import MongoClient

__author__ = "Yiwen Sun and Ziyou Zhang"
__status__ = "Prototype"
      
def test_data_vlidity():
    with MongoClient('mongodb://admin:sentrade@45.76.133.175:27017') as client:
        db = client.sentrade_db
        stock_db = db.stock_price
        all_stock = stock_db.find()
        for stock in all_stock:
            assert stock['open'] >= 0
            assert stock['high'] >= 0
            assert stock['low'] >= 0 
            assert stock['close'] >= 0
            assert stock['volume'] >= 0

if __name__ == "__main__":
    pass