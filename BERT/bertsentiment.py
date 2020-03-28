#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Davide Locatelli, Ziyou Zhang"
__status__ = "Production"

import sys
from bert_predict import predict_score
from pymongo import MongoClient
from pymongo import errors

def bert_sentiment_database(company_name, client_address):
    """
    Ananlyse the BERT sentiment scores and add them in the database.

    :param company_name: the name of the company. Used as the entry in the database.
    """
    client = MongoClient(client_address)
    twitter_db = client.twitter_data

    count = 0
    total_count = twitter_db[company_name].count_documents({})
    
    for news in twitter_db[company_name].find().batch_size(100):
        try:
            score = predict_score(news["processed_text"])
            bert_polarity = {"$set": {"bert_polarity": score}}
            twitter_db[company_name].update_one(news, bert_polarity)
            count += 1
            print("analyse", company_name, "progress:", count, "/", total_count)
        except errors.CursorNotFound:
            count += 1
            print("skip analyse", company_name, "progress:", count, "/", total_count)
    
    client.close()

def generate_bert_sentiment_database(company_name, client_address):
    """
    Calculate the bert sentiment scores and put them into the database.

    :param company_name: the name of the company. Used as the entry in the database.
    """
    client = MongoClient(client_address)
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
        # sum all scores
        for company_tweet in twitter_db[company_name].find({"date": date}):
            if "bert_polarity" in company_tweet:
                news_score += company_tweet["bert_polarity"]
                news_count += 1
        # check if the date is not yet in the database
        if (sentiment_db[company_name].count_documents({"date": date}) == 0):
            sentiment = {"company": company_name,
                         "date": date,
                         "1_day_bert_sentiment_score": news_score / news_count,
                         "1_day_overall_bert_sentiment_score": news_score}
            sentiment_db[company_name].insert_one(sentiment)
        else:
            updated_sentiment_score = {"$set": {"1_day_bert_sentiment_score": news_score / news_count,
                                                "1_day_overall_bert_sentiment_score": news_score}}
            sentiment_db[company_name].update_one(sentiment_db[company_name].find_one({"date": date}), updated_sentiment_score)
        progress_count += 1
        print("summarise", company_name, "progress:", progress_count, "/", progress_full)
        
    client.close()

if __name__ == "__main__":
    client_address = "mongodb://admin:sentrade@45.76.133.175:27017"
    # companies = ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]
    unambiguous_companies = ["facebook", "google", "microsoft", "netflix", "tesla", "uber"]
    for company in unambiguous_companies:
        # bert_sentiment_database(company, client_address)
        generate_bert_sentiment_database(company, client_address)