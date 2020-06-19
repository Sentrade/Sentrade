#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Yiwen Sun and Ziyou Zhang"
__status__ = "Production"

import pytest
from pymongo import MongoClient

      
def test_data_vlidity():
    with MongoClient(os.environ["CLIENT_ADDR"]) as client:
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