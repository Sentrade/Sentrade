from tw_funcs import search_keyword_db

import calendar
import glob
import json
import pymongo
import os
from tw_funcs import nlp_process

# db_client = pymongo.MongoClient(os.environ["CLIENT_ADDR"])
# db = db_client["twitter_data"]
# filename = "16/19/31.json"
# year = 2019
# month = 9
# day = 16
# month_abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
# keyword_list = ["netflix", "amazon", "apple", "microsoft", "google", "tesla", "facebook"]

# for filename in glob.glob("./collection/*/*/*.json", recursive=True):
# 	print(filename)
# 	keyword = filename.split('_')[0].split('/')[-1]
# 	[year, month, day] = filename.split('_')[-1].split('-')
# 	day = day.split('.')[0]
# 	with open(filename, 'r') as f:
# 		data = [json.loads(line) for line in f]

# 	result = []
# 	for item in data:
# 		text = nlp_process(item["text"])
# 		item = {remained_key: item[remained_key] for remained_key in ["id", "created_at", "source", "text"]}
# 		item["original_text"] = item.pop("text")
# 		date_info = item["created_at"].split()
# 		item["processed_text"] = text
# 		item["date"] = str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
# 		result.append(item)

# 	if result:
# 		db[keyword].insert(result)

# for keyword in keyword_list:
# 	search_keyword_db(keyword, filename, db, year, month, month_abbr_to_num)

try:
	f = open("./nonexist.txt", 'r')
except Exception as e:
	print("Exception")
	print(e)