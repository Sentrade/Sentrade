#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Davide Locatelli, Ziyou Zhang"
__status__ = "Production"

import json
import sys
import spacy
import os
from datetime import datetime, timedelta
from dateutil.parser import parse
from textblob import TextBlob
from pymongo import MongoClient
from pymongo import errors

def get_date_offset(date, offset):
    """
    Get the string representing the date with certain offset.

    :param date: the date string, with the format of YYYY-MM-DD.
    :param offset: date difference.
    :return: the string representing the date with the offset difference.
    """

    date_object = datetime.strptime(date, "%Y-%m-%d")
    date_offset = (date_object - timedelta(offset)).strftime("%Y-%m-%d")
    return date_offset
    
def is_org(news, company_name):
    """
    Function to check if a company is named in a piece of news

    :param news: the news being checked (in JSON format)
    :param company_name: the name of the company (lowercase)
    :return: true if the company is named, false otherwise.
    """

    nlp = spacy.load("en_core_web_sm") #create a spaCy Language object
    doc = nlp(news["text"]) #select text of the news
    for t in doc.ents:
        if t.lower_ == company_name: #if company name is called
            if t.label_ == "ORG" or t.label_ == "PRODUCT": #check they actually mean the company
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

def raw_blob_analysis(inputfile, outputfile):
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

def blob_sentiment_database(company_name, client_address):
    """
    Ananlyse the textblob sentiment scores and add them in the database.

    :param company_name: the name of the company. Used as the entry in the database.
    :param client_address: the address of the database.
    """

    client = MongoClient(client_address)
    twitter_db = client.twitter_data

    count = 0
    total_count = twitter_db[company_name].count_documents({})
    for news in twitter_db[company_name].find().batch_size(1000):
        try:
            blob = TextBlob(news["processed_text"])
            updated_polarity = {"$set": {"polarity": blob.sentiment.polarity}}
            updated_subjectivity = {"$set": {"subjectivity": blob.sentiment.subjectivity}}
            twitter_db[company_name].update_one(news, updated_polarity)
            twitter_db[company_name].update_one(news, updated_subjectivity)
            count += 1
            print("analyse", company_name, "progress:", count, "/", total_count)
        except errors.CursorNotFound:
            count += 1
            print("skip analyse", company_name, "progress:", count, "/", total_count)
    
    client.close()

def generate_blob_sentiment_database(company_name, client_address):
    """
    Calculate the textblob sentiment scores and put them into the database.

    :param company_name: the name of the company. Used as the entry in the database.
    :param client_address: the address of the database.
    """

    client = MongoClient(client_address)
    db = client.sentrade_db
    twitter_db = client.twitter_data
    sentiment_db = client.sentiment_data

    all_date = twitter_db[company_name].distinct("date")

    progress_full = len(all_date)
    progress_count = 0
    for date in all_date:
        news_score = 0  
        news_count = sys.float_info.epsilon
        # sum all scores
        for company_tweet in twitter_db[company_name].find({"date": date}):
            if "polarity" in company_tweet:
                # get rid of the neutral results
                # if company_tweet["polarity"] < -0.3 or company_tweet["polarity"] > 0.3:
                news_score += company_tweet["polarity"]
                news_count += 1
        # check if the date is not yet in the database
        if (sentiment_db[company_name].count_documents({"date": date}) == 0):
            sentiment = {"company": company_name,
                         "date": date,
                         "today_sentiment_score": news_score / news_count,
                         "today_overall_sentiment_score": news_score,
                         "today_news_count": news_count}
            sentiment_db[company_name].insert_one(sentiment)
        else:
            updated_sentiment_score = {"$set": {"today_sentiment_score": news_score / news_count,
                                                "today_overall_sentiment_score": news_score,
                                                "today_news_count": news_count}}
            sentiment_db[company_name].update_one(sentiment_db[company_name].find_one({"date": date}), updated_sentiment_score)
        progress_count += 1
        print("summarise", company_name, "progress:", progress_count, "/", progress_full)
        
    client.close()

def extend_blob_sentiment_database(company_name, client_address):
    """
    Calculate the 1 day, 3 days and 7 days textblob sentiment scores based on 1 day sentiment average.
    Perform this operation only after today sentiment score is obtained.

    :param company_name: the name of the company. Used as the entry in the database.
    :param client_address: the address of the database.
    """

    client = MongoClient(client_address)
    sentiment_db = client.sentiment_data

    news_dates = []
    news_scores = []

    all_date = sentiment_db[company_name].distinct("date")

    progress_full = len(all_date)
    progress_count = 0
    for date in all_date:

        # calculate past 1 day sentiment scores
        one_day_news_score = 0  
        one_day_news_count = sys.float_info.epsilon
        for i in range(1, 2):
            current_day = sentiment_db[company_name].find_one({"date": get_date_offset(date, i)})
            if current_day:
                one_day_news_score += current_day["today_overall_sentiment_score"]
                one_day_news_count += current_day["today_news_count"]

        updated_sentiment_score = {"$set": {"1_day_sentiment_score": one_day_news_score / one_day_news_count,
                                            "1_day_overall_sentiment_score": one_day_news_score,
                                            "1_day_news_count": one_day_news_count}}
        sentiment_db[company_name].update_one(sentiment_db[company_name].find_one({"date": date}), updated_sentiment_score)

        
        # calculate past 3 day sentiment scores
        three_day_news_score = 0  
        three_day_news_count = sys.float_info.epsilon

        for i in range(1, 4):
            current_day = sentiment_db[company_name].find_one({"date": get_date_offset(date, i)})
            if current_day:
                three_day_news_score += current_day["today_overall_sentiment_score"]
                three_day_news_count += current_day["today_news_count"]

        updated_sentiment_score = {"$set": {"3_day_sentiment_score": three_day_news_score / three_day_news_count,
                                            "3_day_overall_sentiment_score": three_day_news_score,
                                            "3_day_news_count": three_day_news_count}}
        sentiment_db[company_name].update_one(sentiment_db[company_name].find_one({"date": date}), updated_sentiment_score)

        # calculate past 7 day sentiment scores
        seven_day_news_score = 0  
        seven_day_news_count = sys.float_info.epsilon

        for i in range(1, 8):
            current_day = sentiment_db[company_name].find_one({"date": get_date_offset(date, i)})
            if current_day:
                seven_day_news_score += current_day["today_overall_sentiment_score"]
                seven_day_news_count += current_day["today_news_count"]

        updated_sentiment_score = {"$set": {"7_day_sentiment_score": seven_day_news_score / seven_day_news_count,
                                            "7_day_overall_sentiment_score": seven_day_news_score,
                                            "7_day_news_count": seven_day_news_count}}
        sentiment_db[company_name].update_one(sentiment_db[company_name].find_one({"date": date}), updated_sentiment_score)

        progress_count += 1
        print("extend", company_name, "progress:", progress_count, "/", progress_full)
        
    client.close()

if __name__ == "__main__":
    client_address = os.environ["CLIENT_ADDR"]
    companies = ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]
    
    for company in companies:
        # blob_sentiment_database(company, client_address)
        generate_blob_sentiment_database(company, client_address)
        extend_blob_sentiment_database(company, client_address)
