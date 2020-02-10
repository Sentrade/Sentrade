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
hour = 19
minute = 31

tw_filename = "./{0}/{1}/{2}.json".format(str(day).zfill(2), str(hour).zfill(2), str(minute).zfill(2))
with open(tw_filename, 'r') as f:
	data = [json.loads(line) for line in f]

keyword = "Apple"
time = "{0}-{1}-{2}-{3}-{4}".format(year, str(month).zfill(2), str(day).zfill(2), str(hour).zfill(2), str(minute).zfill(2))
tw_text_file = open("./{0}.txt".format(time), 'w')
tw_text_file_keyword = open("./{0}_{1}.txt".format(keyword, time), 'w')
tw_text_file_keyword_processed = open("./{0}_proc_{1}.txt".format(keyword, time), 'w')
tw_text_file_lang_detect_err = open("./lang_err_{0}.txt".format(time), 'w')
en_corpus = set(nltk.corpus.words.words())

for item in data:
	# print(type(item)) # type: 'dict'
	if "text" in item.keys():
		text = item["text"]
		tw_text_file.write(text)
		if re.search(re.compile(keyword), text):
			try:
				if (TextBlob(text).detect_language() == 'en'):
					tw_text_file_keyword.write(text)
					pure_en_text = ""
					for w in nltk.wordpunct_tokenize(text):
						if w.lower() in en_corpus:
							# w.isalpha():
							pure_en_text = pure_en_text + w + ' '
					tw_text_file_keyword_processed.write(pure_en_text)
			except:
				tw_text_file_lang_detect_err.write(text)
		

