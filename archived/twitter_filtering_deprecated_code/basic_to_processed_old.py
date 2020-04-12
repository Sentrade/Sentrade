__author__ = "Fengming Liu"
__status__ = "prototype"

import json
import nltk
import subprocess
import re
import emoji
import tw_funcs

def process_basic_data(date, keyword):

	tw_text_file_keyword = open("./collection/basic/{0}_{1}.json".format(keyword, date), 'r')
	# subprocess.run("rm " + "./collection/basic/{0}_{1}_processed.json".format(keyword, date), shell=True)
	tw_text_file_keyword_processed = open("./collection/processed/{0}_{1}_processed.json".format(keyword, date), 'a')

	procitem = {}
	for item in [json.loads(line) for line in tw_text_file_keyword]:
		# text = item["text"]
		# print("<Original>" + text)

		# remove RT username, hyperlinks, emoji
		# text = re.sub(pattern=re.compile(r'RT @(.*?):(\s)'), repl='', string=text)
		# text = re.sub(pattern=re.compile(r'http\S+'), repl='', string=text)
		# text = re.sub(pattern=emoji.get_emoji_regexp(), repl='', string=text)
		# text = "".join([i if ord(i) < 128 else '' for i in text])

		# remove non-English characters
		# text = " ".join(w for w in nltk.wordpunct_tokenize(text) if w.lower() in en_corpus or not w.isalpha())
		
		# print("<Processd>" + text)
		# print()
		# extract useful fields and dump into json file
		# procitem["id"] = item["id"]
		# procitem["created_at"] = item["created_at"]
		# procitem["source"] = item["source"]
		# procitem["text"] = text
		item = {remained_key: item[remained_key] for remained_key in ["id", "created_at", "source", "text"]}
		item["text"] = tw_funcs.remove_extra_char(item["text"])
		json.dump(item, tw_text_file_keyword_processed)
		tw_text_file_keyword_processed.write('\n')

	tw_text_file_keyword.close()
	tw_text_file_keyword_processed.close()

year = 2019
month = 9
day = 16
keyword_list = ["netflix", "amazon", "apple", "microsoft", "google", "tesla", "facebook"]
date = "{0}-{1}-{2}".format(year, str(month).zfill(2), str(day).zfill(2))
for keyword in keyword_list:
	process_basic_data(date, keyword)