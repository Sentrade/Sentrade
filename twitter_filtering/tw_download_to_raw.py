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

def search_keyword(keyword, filename, local_dir, date_filename, run_log):
	run_log.write("Searching for the keyword " + keyword + '\n')
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

def process_bz2(tw_json_bz2_filename, run_log):
	run_log.write("Extracting the bz2 file " + tw_json_bz2_filename + '\n')
	subprocess.run("bunzip2 -k " + tw_json_bz2_filename, shell=True)
	subprocess.run("rm " + tw_json_bz2_filename, shell=True)

	# construct the local directory containing the result
	local_dir = "./subjecet_tw/raw/"
	if not os.path.exists(local_dir):
		os.makedirs(local_dir)

	# search keywords in the file
	tw_json_filename = tw_json_bz2_filename.split('.')[0] + ".json"
	keyword_list = ["netflix", "amazon", "apple", "microsoft", "google", "tesla", "facebook"]
	for keyword in keyword_list:
		search_keyword(keyword, tw_json_filename, local_dir, "{0}-{1}-{2}.json".format(year, month.zfill(2), day.zfill(2)), run_log)
	subprocess.run("rm " + tw_json_filename, shell=True)

def download_archive(year, month, day, run_log):
	http = urllib3.PoolManager()
	url = "https://ia803103.us.archive.org/7/items/archiveteam-twitter-stream-{0}-{1}/twitter_stream_{2}_{3}_{4}.tar".format(year, month, year, month, day)
	with http.request('GET', url, preload_content=False) as response, open("./twitter_stream_{0}_{1}_{2}.tar".format(year, month, day), 'wb') as out_file:
		if response.status == 404:
			return False
		else:
			run_log.write("Downloading the tar file\n")
			shutil.copyfileobj(response, out_file)
			return True

year = 2019
month = 1
run_log = open("./running.log", 'a')
for day in range(1, 32):
	# downlaod archive zip
	date = "{0}_{1}_{2}".format(year, str(month).zfill(2), str(day).zfill(2))
	date_tar_filename = "./twitter_stream_{0}.tar".format(date)
	if download_archive(year, str(month).zfill(2), str(day).zfill(2), run_log) == False:
		subprocess.run("rm " + date_tar_filename, shell=True)
		continue

	# extract bz2 files
	date_tar = tarfile.open(date_tar_filename, 'r')
	for mem in date_tar.getmembers():
		# start time
		time_log = open("./{0}.log".format(date), 'a')
		start_tick = time.time()

		# extract the member out
		if mem.isfile():
			date_tar.extract(mem)
		else:
			continue

		# unzip the bz2 file to json file
		tw_json_bz2_filename = mem.name
		process_bz2(tw_json_bz2_filename, run_log)

		# end time
		end_tick = time.time()
		time_log.write("{0:15s}	{1:.3f}\n".format(tw_json_filename, end_tick - start_tick))
		time_log.close()

	# remove tar file and empty folder
	date_tar.close()
	subprocess.run("rm " + date_tar_filename, shell=True)
	subprocess.run("rm -rf ./{0}".format(str(day).zfill(2)), shell=True)

run_log.close()