__author__ = "Fengming Liu"
__status__ = "prototype"

import json
import nltk
import subprocess
import re
import emoji
import tw_funcs
import os

def process_basic_data(date, keyword, basic_dir, processed_dir):
	tw_basic = open(basic_dir + "{0}_{1}.json".format(keyword, date), 'r')
	tw_processed_filename = processed_dir + "{0}_{1}_processed.json".format(keyword, date)
	if os.path.exists(tw_processed_filename):
		subprocess.run("rm " + tw_processed_filename, shell=True)
	tw_processed = open(tw_processed_filename, 'a')

	for item in [json.loads(line) for line in tw_basic]:
		item = {remained_key: item[remained_key] for remained_key in ["id", "created_at", "source", "text"]}
		item["text"] = tw_funcs.remove_extra_char(item["text"])
		json.dump(item, tw_processed)
		tw_processed.write('\n')

	tw_basic.close()
	tw_processed.close()

year = 2019
month = 9
day = 16
keyword_list = ["netflix", "amazon", "apple", "microsoft", "google", "tesla", "facebook"]
date = "{0}-{1}-{2}".format(year, str(month).zfill(2), str(day).zfill(2))
for keyword in keyword_list:
	process_basic_data(date, keyword, "./collection/basic/", "./collection/processed/")