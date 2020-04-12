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
		try:
			data = [json.loads(line) for line in f]
		except:
			print("problem in reading json file", filename)
			return

	# write the selected items into a new json file
	result = []
	for item in data:
		keys = item.keys()
		if "text" in keys and "lang" in keys and item["lang"] == "en":
			try:
				text = nlp_process(item["text"])
			except:
				print("problem in text processing", filename)
				continue

			try:
				if re.search(re.compile(keyword), text): # search based on the lower case
					item = {remained_key: item[remained_key] for remained_key in ["id", "created_at", "source", "text"]}
					item["original_text"] = item.pop("text")
					date_info = item["created_at"].split()
					item["processed_text"] = text
					item["date"] = str(year) + '-' + str(month).zfill(2) + '-' + filename.split('/')[0]
					result.append(item)
			except:
				print("problem in keyword searching", filename)
				continue
	if result:
		db[keyword].insert(result)


def download_archive(year, month, day):
	http = urllib3.PoolManager()
	url = "https://ia803103.us.archive.org/7/items/archiveteam-twitter-stream-{0}-{1}/twitter_stream_{2}_{3}_{4}.tar".format(year, month, year, month, day)
	print(url)
	with http.request('GET', url, preload_content=False) as response, open("./twitter_stream_{0}_{1}_{2}.tar".format(year, month, day), 'wb') as out_file:
		print(response.status)
		if response.status == 404:
			return False
		else:
			print("Downloading the tar file ./twitter_stream_{0}_{1}_{2}.tar".format(year, month, day))
			shutil.copyfileobj(response, out_file)
			return True