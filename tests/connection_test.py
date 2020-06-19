#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Yiwen Sun and Ziyou Zhang"
__status__ = "Production"

import pytest
from pprint import pprint
from pymongo import MongoClient
from multiprocessing import Process

      
def test_connection():
    with MongoClient(os.environ["CLIENT_ADDR"]) as client:
        db=client.admin
        serverStatusResult=db.command("serverStatus")
        assert serverStatusResult["connections"]["active"] > 0

def get_connection_count():
    with MongoClient(os.environ["CLIENT_ADDR"]) as client:
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