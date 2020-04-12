__author__ = "Fengming Liu"
__status__ = "prototype"

import pymongo

db_client = pymongo.MongoClient("mongodb://admin:sentrade@127.0.0.1", 27017)
db = db_client["sentrade_db"]
collection = db["stock_price"]

for record in collection.find():
	print(record)
