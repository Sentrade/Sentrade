__author__ = "Fengming Liu"
__status__ = "prototype"

import tarfile
import json
import re

year = 2019
month = 9
day = 16
hour = 19
minute = 31

tw_filename = "./{0}/{1}/{2}.json".format(str(day).zfill(2),str(hour).zfill(2),str(minute).zfill(2))

with open(tw_filename, 'r') as f:
	data = [json.loads(line) for line in f]

keyword = "Apple"
tw_text_file = open("./{0}_{1}-{2}-{3}-{4}-{5}.txt".format(keyword, year, str(month).zfill(2), str(day).zfill(2),str(hour).zfill(2),str(minute).zfill(2)), 'w')

for item in data:
	# print(type(item)) # type: 'dict'
	if "text" in item.keys():
		text = item["text"]
		if re.search(re.compile(keyword), text):
			tw_text_file.write(text)