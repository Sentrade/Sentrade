__author__ = "Fengming Liu"
__status__ = "prototype"

import tarfile
import subprocess
import time
import os
import json
import re
import sys
import urllib3
import shutil

def search_keyword(keyword, filename, local_dir, date_filename):
	print("Searching for the keyword", keyword)
	tw_text_file_keyword = open(local_dir + keyword + "_" + date_filename, 'a')
	
	# load the data into the memory
	with open(filename, 'r') as f:
		data = [json.loads(line) for line in f]

	# write the selected items into a new json file
	for item in data:
		keys = item.keys()
		if "text" in keys and "lang" in keys and item["lang"] == "en":
			if re.search(re.compile(keyword), item["text"].lower()): # search based on the lower case
				json.dump(item, tw_text_file_keyword)
				tw_text_file_keyword.write('\n')
	tw_text_file_keyword.close()

def download_archive(year, month, day):
	http = urllib3.PoolManager()
	url = "https://ia803103.us.archive.org/7/items/archiveteam-twitter-stream-{0}-{1}/twitter_stream_{2}_{3}_{4}.tar".format(year, month, year, month, day)
	with http.request('GET', url, preload_content=False) as response, open("./twitter_stream_{0}_{1}_{2}.tar".format(year, month, day), 'wb') as out_file:
		shutil.copyfileobj(response, out_file)

year = 2019
month in range(1, 13):
	day in range(1, 32):



date = "{0}_{1}_{2}".format(year, month.zfill(2), day.zfill(2))
date_tar = tarfile.open("./twitter_stream_{0}.tar".format(date), 'r')

for mem in date_tar.getmembers():
	# start time
	time_log = open("./keyword_search_time.log", 'a')
	start_tick = time.time()

	# extract the member out
	if mem.isfile():
		date_tar.extract(mem)
	else:
		continue

	# unzip the bz2 file to json file
	tw_json_bz2_filename = mem.name
	subprocess.run("bunzip2 -k " + tw_json_bz2_filename, shell=True)
	subprocess.run("rm " + tw_json_bz2_filename, shell=True)

	# construct the local directory containing the result
	local_dir = "./subjecet_tw/raw/"
	if not os.path.exists(local_dir):
		os.makedirs(local_dir)

	# search keywords in the file
	tw_json_filename = tw_json_bz2_filename.split('.')[0] + ".json"
	print(tw_json_filename)
	keyword_list = ["netflix", "amazon", "apple", "microsoft", "google", "tesla", "facebook"]
	for keyword in keyword_list:
		search_keyword(keyword, tw_json_filename, local_dir, "{0}-{1}-{2}.json".format(year, month.zfill(2), day.zfill(2)))
	subprocess.run("rm " + tw_json_filename, shell=True)

	# end time
	end_tick = time.time()
	time_log.write("{0:15s}	{1:.3f}\n".format(tw_json_filename, end_tick - start_tick))
	time_log.close()