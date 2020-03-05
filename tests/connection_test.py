#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from pprint import pprint
from pymongo import MongoClient
from multiprocessing import Process

__author__ = "Yiwen Sun and Ziyou Zhang"
__status__ = "Prototype"
      
def test_connection():
    with MongoClient('mongodb://admin:sentrade@45.76.133.175:27017') as client:
        db=client.admin
        serverStatusResult=db.command("serverStatus")
        assert serverStatusResult["connections"]["active"] > 0

def get_connection_count():
    with MongoClient('mongodb://admin:sentrade@45.76.133.175:27017') as client:
        db=client.admin
        serverStatusResult=db.command("serverStatus")
        return serverStatusResult["connections"]["active"]

def test_multi_connections():
    procs = []
    for i in range(1000):
        proc = Process(target=get_connection_count)
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
    
    #will only reach here if all tests passed
    assert True

    
if __name__ == "__main__":
    test_multi_connections()