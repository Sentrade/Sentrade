__author__ = "Fengming Liu"
__status__ = "prototype"

import pymongo

db_client = pymongo.MongoClient(os.environ["CLIENT_ADDR"])
db = db_client["sentrade_db"]
collection = db["stock_price"]

for record in collection.find():
	print(record)
