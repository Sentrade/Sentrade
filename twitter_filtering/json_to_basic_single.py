__author__ = "Fengming Liu"
__status__ = "prototype"

import tarfile
import subprocess
import time
import os
import json
import re
import sys

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

year = 2019
month = 9
day = sys.argv[1].zfill(2)
hour = sys.argv[2].zfill(2)
minute = sys.argv[3].zfill(2)
local_dir = sys.argv[4]

# start time
# time_log = open("./keyword_search_time.log", 'a')
# start_tick = time.time()

# search keywords in the file
tw_json_filename = "./{0}/{1}/{2}.json".format(day, hour, minute)
print(tw_json_filename)
keyword_list = ["netflix", "amazon", "apple", "microsoft", "google", "tesla", "facebook"]
for keyword in keyword_list:
	search_keyword(keyword, tw_json_filename, local_dir, "{0}-{1}-{2}.json".format(year, str(month).zfill(2), day))
# subprocess.run("rm " + tw_json_filename, shell=True)

# end time
# end_tick = time.time()
# time_log.write("{0:15s}	{1:.3f}\n".format(tw_json_filename, end_tick - start_tick))
# time_log.close()