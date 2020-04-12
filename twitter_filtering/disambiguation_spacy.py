__author__ = "Fengming Liu"
__status__ = "prototype"

import pymongo
import spacy
import sys

def is_org(lang_obj, text, company_name):
    """
    Function to check if a company is named in a piece of news

    :param lang_obj: the sapCy language object
    :param text: the news being checked (in string)
    :param company_name: the name of the company (lowercase)
    :returns: true if the company is named, false otherwise
    """
    
    doc = nlp(text) #select text of the news
    for t in doc.ents:
    	# print(t)
    	if t.lower_ == company_name: #if company name is called
    		if t.label_ == "ORG": #check they actually mean the company
    			return True
    return False

    
# essential variables
db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
# db_client = pymongo.MongoClient("mongodb://admin:sentrade@127.0.0.1", 27017)
db_original = db_client["twitter_data"]
print("connected")

keyword_list = ["amazon", "apple", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]
lang_obj = sys.argv[1]
company = sys.argv[2]

if not company in keyword_list:
	print(company + " can't be processed")
	exit(0)
	
if lang_obj == 'sm':
	nlp = spacy.load("en_core_web_sm") #create a spaCy Language object
	db_filtered = db_client["twitter_filtered"]
elif lang_obj == 'md':
	nlp = spacy.load("en_core_web_md") #create a spaCy Language object
	db_filtered = db_client["twitter_filtered_spacy_md"]
elif lang_obj == 'lg':
	nlp = spacy.load("en_core_web_lg") #create a spaCy Language object
	db_filtered = db_client["twitter_filtered_spacy_lg"]
else:
	print("no such language model")
	exit(0)


for record in db_original[company].find():
	try:
		if is_org(nlp, record["processed_text"], company):
			db_filtered[company].insert(record)
	except Exception as e:
		print("Problem in processing:", record["_id"])
		print(e)

print(company + " finished")