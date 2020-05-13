__author__ = "Fengming Liu"
__status__ = "prototype"

import pymongo
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize
import sys
    
# essential variables
db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
# db_client = pymongo.MongoClient("mongodb://admin:sentrade@127.0.0.1", 27017)
db_original = db_client["twitter_data"]
db_filtered = db_client["twitter_NER"]
print("connected")

company_list = ["amazon", "apple", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]
st = StanfordNERTagger("./stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz",
					   "./stanford-ner-2018-10-16/stanford-ner.jar")

for company in company_list:
	for record in db_original[company].find():
		# for sent in sent_tokenize(record["processed_text"]):
		tokens = word_tokenize(record["processed_text"])
		tags = st.tag(tokens)
		for tag in tags:
			if tag[0] == company and tag[1]=='ORGANIZATION':
				db_filtered[company].insert(record)
				break
