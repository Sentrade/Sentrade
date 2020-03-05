__author__ = "Fengming Liu"
__status__ = "prototype"

import tarfile
import subprocess
import time
import os
import json
import re
import sys
import tw_funcs

year, month, day = sys.argv[1], sys.argv[2], sys.argv[3]
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
		tw_funcs.search_keyword(keyword, tw_json_filename, local_dir, "{0}-{1}-{2}.json".format(year, month.zfill(2), day.zfill(2)))
	subprocess.run("rm " + tw_json_filename, shell=True)

	# end time
	end_tick = time.time()
	time_log.write("{0:15s}	{1:.3f}\n".format(tw_json_filename, end_tick - start_tick))
	time_log.close()