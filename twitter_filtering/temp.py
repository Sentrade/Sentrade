from tw_funcs import search_keyword_db

import pymongo
import os
import json

db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
db = db_client["temp"]

search_keyword_db("facebook", "./16/19/31.json", "./collection/to_db/", db)
search_keyword_db("google", "./16/19/31.json", "./collection/to_db/", db)
search_keyword_db("netflix", "./16/19/31.json", "./collection/to_db/", db)
search_keyword_db("tesla", "./16/19/31.json", "./collection/to_db/", db)
search_keyword_db("microsoft", "./16/19/31.json", "./collection/to_db/", db)