import pymongo
from sshtunnel import SSHTunnelForwarder

db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
db = db_client["sentrade_db"]
collection = db["stock_price"]

for record in collection.find():
	print(record)
