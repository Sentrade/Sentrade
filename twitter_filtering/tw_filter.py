__author__ = "Fengming Liu"
__status__ = "prototype"

import tarfile
import json
import re
from textblob import TextBlob
import nltk

year = 2019
month = 9
day = 16
keyword = "Apple"
# en_corpus = set(nltk.corpus.words.words())
date = "{0}-{1}-{2}".format(year, str(month).zfill(2), str(day).zfill(2))
tw_text_file_keyword = open("./{0}_{1}.json".format(keyword, date), 'a')
# with open("./all_files.txt", 'r') as f_list:
# 	for tw_filename in f_list:

for hour in range(6, 24):
	for minute in [30]:
		tw_filename = "./{0}/{1}/{2}.json".format(str(day).zfill(2), str(hour).zfill(2), str(minute).zfill(2))
		# load the json file into the memory
		with open(tw_filename, 'r') as f:
			data = [json.loads(line) for line in f]

		# write the selected items into a new json file
		for item in data:
			keys = item.keys()
			if "text" in keys and "lang" in keys and item["lang"] == "en":
				text = item["text"]
				if re.search(re.compile(keyword), text):
					json.dump(item, tw_text_file_keyword)
					tw_text_file_keyword.write('\n')

tw_text_file_keyword.close()


# with open("./{0}_{1}.json".format(keyword, date), 'r') as f:
# 	data = [json.loads(line) for line in f]
# count = 0
# for item in data:
# 	count = count + 1
# 	print(count)