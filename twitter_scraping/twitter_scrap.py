#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy as tw
import pandas as pd
import json
import re
from datetime import datetime
from textblob import TextBlob

__author__ = "Ziyou Zhang, Fenming Liu"
__status__ = "Development"

month_map = {"Jan": "01", 
             "Feb": "02",
             "Mar": "03",
             "Apr": "04",
             "May": "05",
             "Jun": "06",
             "Jul": "07",
             "Aug": "08",
             "Sep": "09",
             "Oct": "10",
             "Nov": "11",
             "Dec": "12"
            }

def parse_twitter_date(date):
    """
    Change the format of the twitter date string.

    :param date: the original date string. e.g. "Fri Jan 03 16:34:09 +0000 2020"
    
    :return: reformated string. e.g. 2020-01-03
    """
    new_date = ""
    
    year = date[-4:]
    month = date[4:7]
    day = date[8:10]
    month = month_map[month]

    new_date = year + "-" + month + "-" + day
    return new_date

def process_original_tweet(text):
    """
    Process the original text.

    :param text: original tweet text.
    :return: the processed tweet text.
    """

    text = re.sub(pattern=re.compile(r'RT @(.*?):(\s)'), repl='', string=text)
    text = re.sub(pattern=re.compile(r'http\S+'), repl='', string=text)
    text = re.sub(pattern=emoji.get_emoji_regexp(), repl='', string=text)
    text = "".join([i if i.isalnum() or i in string.whitespace else '' for i in text])
    text = text.lower()

    return text

def scrap_tweets_today(company_name):
    consumer_key = "o62Qbz4RQcWoSlZwYAf8rk6Br"
    consumer_secret = "rIA9adduzHxl6lude0lCNYoyNy00trNTsGmrlHNR1M5anasaeB"
    access_token = "1079882101191778305-UxW9ONHBCHTsHYlfBcWBqsNVmJ7a70"
    access_token_secret = "0TSs4ls9OYedbFBNhGr72vXgWPkWoFJxDd8Fwj8TpT9jD"

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tw.API(auth)

    search = company_name + " -filter:retweets"
    date_since = datetime.today().strftime('%Y-%m-%d')

    tweets = tw.Cursor(api.search,
                        q=search,
                        lang="en",
                        result_type="mixed",
                        since=date_since).items()
    
    results = []
    count = 0

    for tweet in tweets:
        single_tweet = {}
        single_tweet["date"] = str(tweet.created_at)[:10]

        original_text = tweet.text
        processed_text = process_original_tweet(original_text)
        single_tweet["original_text"] = original_text
        single_tweet["processed_text"] = nlp_process(processed_text)
        
        blob = TextBlob(processed_text)
        single_tweet["polarity"] = blob.sentiment.polarity
        single_tweet["subjectivity"] = blob.sentiment.subjectivity

        count += 1
        print(count, single_tweet)

        results.append(single_tweet)
    
    with open("temp.json", "a") as output_file:
        json.dump(results, output_file)

if __name__ == "__main__":
    # companies = ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]
    companies = ["apple"]
    for company in companies:
        scrap_tweets_today(company)

    

    
