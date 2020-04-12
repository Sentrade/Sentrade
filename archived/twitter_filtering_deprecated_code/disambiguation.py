__author__ = "Fengming Liu"
__status__ = "prototype"

import pymongo
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn

# essential variables
# db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
# db_client = pymongo.MongoClient("mongodb://admin:sentrade@127.0.0.1", 27017)
# db_original = db_client["twitter_data"]
# db_filtered = db_client["twitter_filtered"]
# print("connected")

# keyword_list = ["amazon", "apple"]
# keyword = "Amazon"
# synsets = wn.synsets(keyword)
# for ss in wn.synsets(keyword):
# 	print(ss, type(ss), ss.definition())
# 	print(ss.lemmas())
# print(wn.synsets(keyword)[2])

# for record in db_original[keyword].find():
# 	print(lesk(record["processed_text"], keyword))

# tweet = "amazon is a woman"
# match = lesk(tweet, keyword, synsets=[synsets[0], synsets[2]])
# print(match)

# print(lesk(tweet, keyword, synsets=wn.synsets(keyword)))

def is_org(news, company_name):
    """
    Function to check if a company is named in a piece of news

    :param news: the news being checked (in JSON format)
    :param company_name: the name of the company (lowercase)
    :returns: true if the company is named, false otherwise
    """
    nlp = spacy.load("en_core_web_sm") #create a spaCy Language object
    doc = nlp(news["text"]) #select text of the news
    for t in doc.ents:
        if t.lower_ == company_name: #if company name is called
            if t.label_ == "ORG": #check they actually mean the company
                return True
    return False

import spacy