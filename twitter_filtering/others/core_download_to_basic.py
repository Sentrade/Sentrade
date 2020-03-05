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
import tw_funcs

def process_bz2(tw_json_bz2_filename, local_dir, year, month, day):
	print("Extracting the bz2 file " + tw_json_bz2_filename)
	subprocess.run("bunzip2 -k " + tw_json_bz2_filename, shell=True)
	subprocess.run("rm " + tw_json_bz2_filename, shell=True)

	# search keywords in the file
	tw_json_filename = tw_json_bz2_filename.split('.')[0] + ".json"
	keyword_list = ["netflix", "amazon", "apple", "microsoft", "google", "tesla", "facebook"]
	for keyword in keyword_list:
		tw_funcs.search_keyword(keyword, tw_json_filename, local_dir, "{0}-{1}-{2}.json".format(year, str(month).zfill(2), str(day).zfill(2)))
	subprocess.run("rm " + tw_json_filename, shell=True)

def download_archive(year, month, day):
	http = urllib3.PoolManager()
	url = "https://ia803103.us.archive.org/7/items/archiveteam-twitter-stream-{0}-{1}/twitter_stream_{2}_{3}_{4}.tar".format(year, month, year, month, day)
	with http.request('GET', url, preload_content=False) as response, open("./twitter_stream_{0}_{1}_{2}.tar".format(year, month, day), 'wb') as out_file:
		if response.status == 404:
			return False
		else:
			print("Downloading the tar file")
			shutil.copyfileobj(response, out_file)
			return True

year = 2019

# construct the local directory containing the result
local_dir = "./collection/basic/"
if not os.path.exists(local_dir):
	os.makedirs(local_dir)

# for month in range(3, 9):
month = sys.argv[1]
for day in range(1, 32):
	# downlaod archive zip
	date = "{0}_{1}_{2}".format(year, str(month).zfill(2), str(day).zfill(2))
	date_tar_filename = "./twitter_stream_{0}.tar".format(date)

	if not os.path.exists(date_tar_filename):
		if download_archive(year, str(month).zfill(2), str(day).zfill(2)) == False:
			subprocess.run("rm " + date_tar_filename, shell=True)
			continue

	# extract bz2 files
	date_tar = tarfile.open(date_tar_filename, 'r')
	for mem in date_tar.getmembers():
		# start time
		if not os.path.exists("./time_log"):
			os.makedirs("local_dir")
		time_log = open("./time_log/{0}.log".format(date), 'a')
		start_tick = time.time()

		# extract the member out
		if mem.isfile():
			date_tar.extract(mem)
		else:
			continue

		# unzip the bz2 file to json file
		tw_json_bz2_filename = mem.name
		tw_json_filename = tw_json_bz2_filename.split('.')[0] + ".json"
		process_bz2(tw_json_bz2_filename, local_dir, year, month, day)

		# end time
		end_tick = time.time()
		time_log.write("{0:15s}	{1:.3f}\n".format(tw_json_filename, end_tick - start_tick))
		time_log.close()

	# remove tar file and empty folder
	date_tar.close()
	subprocess.run("rm " + date_tar_filename, shell=True)
	subprocess.run("rm -rf ./{0}".format(str(day).zfill(2)), shell=True)