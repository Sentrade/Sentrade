__author__ = "Fengming Liu"
__status__ = "prototype"

import tarfile
import json
import re
import subprocess
import os
import nltk
import time

year = 2019
month = 9
day = 16
keyword_list = ["netflix", "amazon", "apple", "microsoft", "google", "tesla", "facebook"]
date = "{0}-{1}-{2}".format(year, str(month).zfill(2), str(day).zfill(2))
subprocess.run("rm ./keyword_search_time.log", shell=True)
time_log = open("./keyword_search_time.log", 'a')
time_log.write("{0:8s}	{1}\n".format("keyword", "searching time(s)"))


for keyword in keyword_list:
	start_tick = time.time()
	# subprocess.run("rm " + "./subject_tw/raw/{0}_{1}.json".format(keyword, date), shell=True)
	tw_text_file_keyword = open("./subject_tw/raw/{0}_{1}.json".format(keyword, date), 'a')
	# for hour in range(6, 24):
	# 	tw_folder = "./{0}/{1}/".format(str(day).zfill(2), str(hour).zfill(2))
	# 	for filename in os.listdir(tw_folder):
	# 		# load the json file into the memory
	# 		with open(tw_folder + filename, 'r') as f:
	# 			data = [json.loads(line) for line in f]

	# 		# write the selected items into a new json file
	# 		for item in data:
	# 			keys = item.keys()
	# 			if "text" in keys and "lang" in keys and item["lang"] == "en":
	# 				if re.search(re.compile(keyword), item["text"].lower()): # search based on the lower case
	# 					json.dump(item, tw_text_file_keyword)
	# 					tw_text_file_keyword.write('\n')

	tw_text_file_keyword.close()
	end_tick = time.time()
	time_log.write("{0:8s}	{1:.3f}\n".format(keyword, end_tick - start_tick))

time_log.close()