__author__ = "Fengming Liu"
__status__ = "prototype"

import emoji
import json
import nltk
import os
import re
import shutil
import string
import subprocess
import urllib3

def create_dir(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)
	return dir

def nlp_process(text):
	text = re.sub(pattern=re.compile(r'RT @(.*?):(\s)'), repl='', string=text)
	text = re.sub(pattern=re.compile(r'http\S+'), repl='', string=text)
	text = re.sub(pattern=emoji.get_emoji_regexp(), repl='', string=text)
	text = "".join([i if i.isalnum() or i in string.whitespace else '' for i in text])
	text = text.lower()
	return text

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

def process_bz2(tw_json_bz2_filename, keyword_list, local_dir, year, month, day):
	print("Extracting the bz2 file " + tw_json_bz2_filename)
	subprocess.run("bunzip2 -k " + tw_json_bz2_filename, shell=True)
	subprocess.run("rm " + tw_json_bz2_filename, shell=True)

	# search keywords in the file
	tw_json_filename = tw_json_bz2_filename.split('.')[0] + ".json"
	for keyword in keyword_list:
		search_keyword(keyword, tw_json_filename, local_dir, "{0}-{1}-{2}.json".format(year, str(month).zfill(2), str(day).zfill(2)))
	subprocess.run("rm " + tw_json_filename, shell=True)

def process_bz2_db(tw_json_bz2_filename, keyword_list, db, year, month, abbr_to_num):
	print("Extracting the bz2 file " + tw_json_bz2_filename)
	subprocess.run("bunzip2 -k " + tw_json_bz2_filename, shell=True)
	subprocess.run("rm " + tw_json_bz2_filename, shell=True)

	# search keywords in the file
	tw_json_filename = tw_json_bz2_filename.split('.')[0] + ".json"
	for keyword in keyword_list:
		search_keyword_db(keyword, tw_json_filename, db, year, month, abbr_to_num)
	subprocess.run("rm " + tw_json_filename, shell=True)

def search_keyword_db(keyword, filename, db, year, month, abbr_to_num):
	print("Searching for the keyword", keyword)	
	# load the data into the memory
	with open(filename, 'r') as f:
		data = [json.loads(line) for line in f]

	# write the selected items into a new json file
	result = []
	for item in data:
		keys = item.keys()
		if "text" in keys and "lang" in keys and item["lang"] == "en":
			text = nlp_process(item["text"])
			if re.search(re.compile(keyword), text): # search based on the lower case
				item = {remained_key: item[remained_key] for remained_key in ["id", "created_at", "source", "text"]}
				item["original_text"] = item.pop("text")
				date_info = item["created_at"].split()
				# item["date"] = date_info[5] + '-' + str(abbr_to_num[date_info[1]]).zfill(2) + '-' + date_info[2]
				# item["year"] = int(date_info[5])
				# item["month"] = abbr_to_num[date_info[1]]
				# item["day"] = int(date_info[2])
				# clock_info = date_info[3].split(':')
				# item["hour"] = int(clock_info[0])
				# item["minute"] = int(clock_info[1])
				# item["second"] = int(clock_info[2])
				item["processed_text"] = text
				# item["archived_time(US)"] = str(year) + '/' + str(month).zfill(2) + '/' + filename.split('.')[0]
				# item.pop("created_at")
				item["date"] = str(year) + '-' + str(month).zfill(2) + '-' + filename.split('/')[0]
				# print(item)
				result.append(item)
	if result:
		db[keyword].insert(result)


def download_archive(year, month, day):
	http = urllib3.PoolManager()
	url = "https://ia803103.us.archive.org/7/items/archiveteam-twitter-stream-{0}-{1}/twitter_stream_{2}_{3}_{4}.tar".format(year, month, year, month, day)
	with http.request('GET', url, preload_content=False) as response, open("./twitter_stream_{0}_{1}_{2}.tar".format(year, month, day), 'wb') as out_file:
		if response.status == 404:
			return False
		else:
			print("Downloading the tar file ./twitter_stream_{0}_{1}_{2}.tar".format(year, month, day))
			shutil.copyfileobj(response, out_file)
			return True