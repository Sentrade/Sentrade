__author__ = "Fengming Liu"
__status__ = "prototype"

import json
import nltk
import subprocess
import re
import emoji

year = 2019
month = 9
day = 16
keyword = "Apple"
# en_corpus = set(nltk.corpus.words.words())
date = "{0}-{1}-{2}".format(year, str(month).zfill(2), str(day).zfill(2))
tw_text_file_keyword = open("./{0}_{1}.json".format(keyword, date), 'r')
subprocess.run("rm " + "./{0}_{1}_processed.json".format(keyword, date), shell=True)
tw_text_file_keyword_processed = open("./{0}_{1}_processed.json".format(keyword, date), 'a')

procitem = {}
for item in [json.loads(line) for line in tw_text_file_keyword]:
	text = item["text"]
	# print("<Original>" + text)

	# remove RT username, hyperlinks, emoji
	text = re.sub(pattern=re.compile(r'RT @(.*?):(\s)'), repl='', string=text)
	text = re.sub(pattern=re.compile(r'http\S+'), repl='', string=text)
	text = re.sub(pattern=emoji.get_emoji_regexp(), repl='', string=text)
	# text = "".join([i if ord(i) < 128 else '' for i in text])

	# remove non-English characters
	# text = " ".join(w for w in nltk.wordpunct_tokenize(text) if w.lower() in en_corpus or not w.isalpha())
	
	# print("<Processd>" + text)
	# print()
	# extract useful fields and dump into json file
	procitem["id"] = item["id"]
	procitem["created_at"] = item["created_at"]
	procitem["source"] = item["source"]
	procitem["text"] = text
	json.dump(procitem, tw_text_file_keyword_processed)
	tw_text_file_keyword_processed.write('\n')

tw_text_file_keyword.close()
tw_text_file_keyword_processed.close()