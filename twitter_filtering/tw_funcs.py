__author__ = "Fengming Liu"
__status__ = "prototype"

import json
import nltk
import subprocess
import re
import emoji
import string

def remove_extra_char(text):
	text = re.sub(pattern=re.compile(r'RT @(.*?):(\s)'), repl='', string=text)
	text = re.sub(pattern=re.compile(r'http\S+'), repl='', string=text)
	text = re.sub(pattern=emoji.get_emoji_regexp(), repl='', string=text)
	text = "".join([i if i.isalnum() or i in string.whitespace else '' for i in text])
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