__author__ = "Fengming Liu"
__status__ = "prototype"

import pymongo
import os
import json

db_client = pymongo.MongoClient(os.environ["CLIENT_ADDR"])
db = db_client["twitter_data"]

data_folder = "./collection/basic/"
for data_file_name in os.listdir(data_folder):
	data_file = data_folder + data_file_name
	if os.path.isfile(data_file):
		keyword = data_file_name.split('_')[0]
		collection = db[keyword]

		with open(data_file, 'r') as f:
			for line in f:
				collection.insert(json.loads(line))


# keyword_list = ["apple", "amazon", "facebook", "netflix", "microsoft", "tesla", "google"]
# for keyword in keyword_list:
# 	collection = db[keyword]




