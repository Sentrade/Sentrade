#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Davide Locatelli, Ziyou Zhang"
__status__ = "Development"

import json
import spacy
import sys
from textblob import TextBlob
from pymongo import MongoClient
from pymongo import errors

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

def blob_analyse(inputfile, outputfile):
    """
    Function to analyze the sentiment of news about a company using TextBlob
    For each news about the company, a polarity and subjectivity score is added

    :param inputfile: JSON file containing the news to be analyzed
    :param outputfile: JSON file where polarity and subjectivity is outputted
    """    
    with open(inputfile) as news_file:
        input_data= json.load(news_file)

    for news in input_data:
        if is_org(news,company): #if news is about company
            blob = TextBlob(news["text"])
            news["polarity"] = blob.sentiment.polarity
            news["subjectivity"] = blob.sentiment.subjectivity

    with open(outputfile, "w") as results:
        json.dump(input_data, results)

def raw_blob_analysis(inputfile,outputfile):
    """
    Function to analyze the sentiment of news about a company using TextBlob without context checking.

    :param inputfile: JSON file containing the news to be analyzed
    :param outputfile: JSON file where polarity and subjectivity is outputted
    """
    with open(inputfile) as news_file:
        input_data= json.load(news_file)

    for news in input_data:
        blob = TextBlob(news["text"])
        news["polarity"] = blob.sentiment.polarity
        news["subjectivity"] = blob.sentiment.subjectivity

    with open(outputfile, "w") as results:
        json.dump(input_data, results)

def blob_sentiment_database(company_name):
    """
    Ananlyse the textblob sentiment scores and add them in the database.

    :param company_name: the name of the company. Used as the entry in the database.
    """
    client = MongoClient('mongodb://admin:sentrade@45.76.133.175:27017')
    db = client.sentrade_db
    twitter_db = client.twitter_data

    count = 0
    total_count = twitter_db[company_name].count_documents({})
    for news in twitter_db[company_name].find().batch_size(1000):
        try:
            blob = TextBlob(news["processed_text"])
            updated_polarity = {"$set": {"polarity": blob.sentiment.polarity}}
            updated_subjectivity = {"$set": {"subjectivity": blob.sentiment.subjectivity}}
            twitter_db["company_name"].update_one(news, updated_polarity)
            twitter_db["company_name"].update_one(news, updated_subjectivity)
            count += 1
            print("analyse", company_name, "progress:", count, "/", total_count)
        except errors.CursorNotFound:
            count += 1
            print("skip analyse", company_name, "progress:", count, "/", total_count)
    client.close()

def generate_sentiment_database(company_name):
    """
    Calculate the sentiment scores and put them into another database.

    :param company_name: the name of the company. Used as the entry in the database.
    """
    client = MongoClient('mongodb://admin:sentrade@45.76.133.175:27017')
    db = client.sentrade_db
    twitter_db = client.twitter_data
    sentiment_db = client.sentiment_data

    news_dates = []
    news_scores = []
    today_news_count = 0

    all_date = twitter_db[company_name].distinct("date")

    progress_full = len(all_date)
    progress_count = 0
    for date in all_date:
        news_score = 0  
        news_count = sys.float_info.epsilon
        for company_tweet in twitter_db[company_name].find({"date": date}).batch_size(1000):
            if "polarity" in company_tweet:
                news_score += company_tweet["polarity"]
                news_count += 1
        sentiment = {"company": company_name, "date": date, "1_day_sentiment_score": news_score / news_count}
        if (sentiment_db[company_name].find({"date": date}).count() == 0):
            sentiment_db[company_name].insert_one(sentiment)
        else:
            updated_sentiment_score = {"$set": {"1_day_sentiment_score": news_score / news_count}}
            sentiment_db[company_name].update_one(sentiment_db[company_name].find_one({"date": date}), updated_sentiment_score)
        progress_count += 1
        print("summarise", company_name, "progress:", progress_count, "/", progress_full)
        
    client.close()

if __name__ == "__main__":
    companies = ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]
    for company in companies:
        # blob_sentiment_database(company)
        generate_sentiment_database(company)
