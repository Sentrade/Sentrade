#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Davide Locatelli, Ziyou Zhang"
__status__ = "Production"

import time
import sys
from time import ctime
from BertLibrary import BertFTModel
from pymongo import MongoClient, errors

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

def get_model():
    # The BERT model
    ft_model = BertFTModel( model_dir='model',
                        ckpt_name="model.ckpt-35000",
                        labels=['0','1'],
                        lr=1e-05,
                        num_train_steps=30000,
                        num_warmup_steps=1000,
                        ckpt_output_dir='output',
                        save_check_steps=1000,
                        do_lower_case=False,
                        max_seq_len=50,
                        batch_size=32,
                        )

    predictor =  ft_model.get_predictor()
    return predictor

def bert_sentiment_database(company_name, client_address, bert):
    """
    Ananlyse the BERT sentiment scores and add them in the database.

    :param company_name: the name of the company. Used as the entry in the database.
    """
    client = MongoClient(client_address)
    twitter_db = client.twitter_data

    count = 0

    # Count the documents without a BERT score
    total_count = twitter_db[company_name].count_documents({ "bert_sentiment" : { "$exists" : False } })
    start = time.time()
    print("Starting tweet processing for ", company_name)
    for news in twitter_db[company_name].find({ "bert_sentiment" : { "$exists" : False } }).batch_size(1000):
        try:
            text = news["processed_text"]
            scores = bert([text])
            score = scores[0][1]
            score = float("{:.2f}".format(score))
            bert_sentiment = {"$set": {"bert_sentiment": score}}
            twitter_db[company_name].update_one(news, bert_sentiment)
            count += 1
            print("analyse ", company_name, "progress: ", count, "/", total_count)
        except errors.CursorNotFound:
            count += 1
            print("skip analyse ", company_name, "progress: ", count, "/", total_count)
    end = time.time()
    print("Run time for ", total_count, " tweets: ", ctime(end-start))

def generate_bert_sentiment_database(company_name, client_address):
    """
    Calculate the bert sentiment scores and put them into the database.

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
            news_score += company_tweet["bert_sentiment"]
            news_count += 1

        # check if the date is not yet in the database
        if (sentiment_db[company_name].count_documents({"date": date}) == 0):
            sentiment = {"company": company_name,
                         "date": date,
                         "today_bert_sentiment_score": news_score / news_count,
                         "today_overall_bert_sentiment_score": news_score}
            sentiment_db[company_name].insert_one(sentiment)
        else:
            updated_sentiment_score = {"$set": {"today_bert_sentiment_score": news_score / news_count,
                                                "today_overall_bert_sentiment_score": news_score}}
            sentiment_db[company_name].update_one(sentiment_db[company_name].find_one({"date": date}), updated_sentiment_score)
        progress_count += 1
        print("summarise", company_name, "progress:", progress_count, "/", progress_full)
        
    client.close()

def extend_bert_sentiment_database(company_name, client_address):
    """
    Calculate the 1day, 3 days and 7 days bert sentiment scores based on 1 day sentiment average.
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
                one_day_news_score += current_day["today_overall_bert_sentiment_score"]
                one_day_news_count += current_day["today_news_count"]

        updated_sentiment_score = {"$set": {"1_day_bert_sentiment_score": one_day_news_score / one_day_news_count,
                                            "1_day_overall_bert_sentiment_score": one_day_news_score,
                                            "1_day_news_count": one_day_news_count}}
        sentiment_db[company_name].update_one(sentiment_db[company_name].find_one({"date": date}), updated_sentiment_score)

        
        # calculate past 3 day sentiment scores
        three_day_news_score = 0  
        three_day_news_count = sys.float_info.epsilon

        for i in range(1, 4):
            current_day = sentiment_db[company_name].find_one({"date": get_date_offset(date, i)})
            if current_day:
                three_day_news_score += current_day["today_overall_bert_sentiment_score"]
                three_day_news_count += current_day["today_news_count"]

        updated_sentiment_score = {"$set": {"3_day_bert_sentiment_score": three_day_news_score / three_day_news_count,
                                            "3_day_overall_bert_sentiment_score": three_day_news_score,
                                            "3_day_news_count": three_day_news_count}}
        sentiment_db[company_name].update_one(sentiment_db[company_name].find_one({"date": date}), updated_sentiment_score)

        # calculate past 7 day sentiment scores
        seven_day_news_score = 0  
        seven_day_news_count = sys.float_info.epsilon

        for i in range(1, 8):
            current_day = sentiment_db[company_name].find_one({"date": get_date_offset(date, i)})
            if current_day:
                seven_day_news_score += current_day["today_overall_bert_sentiment_score"]
                seven_day_news_count += current_day["today_news_count"]

        updated_sentiment_score = {"$set": {"7_day_bert_sentiment_score": seven_day_news_score / seven_day_news_count,
                                            "7_day_overall_bert_sentiment_score": seven_day_news_score,
                                            "7_day_news_count": seven_day_news_count}}
        sentiment_db[company_name].update_one(sentiment_db[company_name].find_one({"date": date}), updated_sentiment_score)

        progress_count += 1
        print("extend", company_name, "progress:", progress_count, "/", progress_full)
        
    client.close()


if __name__ == "__main__":
    client_address = "mongodb://admin:sentrade@45.76.133.175:27017"
    companies = ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]
    #bert = get_model()
    for company in companies:
        #bert_sentiment_database(company, client_address, bert)
        generate_bert_sentiment_database(company, client_address)
        extend_bert_sentiment_database(company, client_address)