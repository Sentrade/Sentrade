#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy as tw
import pandas as pd
import json
import re

__author__ = "Ziyou Zhang"
__status__ = "Prototype"

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

if __name__ == "__main__":
    consumer_key = "o62Qbz4RQcWoSlZwYAf8rk6Br"
    consumer_secret = "rIA9adduzHxl6lude0lCNYoyNy00trNTsGmrlHNR1M5anasaeB"
    access_token = "1079882101191778305-fTK3WCbG5sBoPKV6prP22YG9rr2EQq"
    access_token_secret = "srrSzTZLEvDYD3wRwjRBf20fTcVCq0I6dfmCgW9G6uCYF"

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tw.API(auth)

    search = "#APPLE -filter:retweets"
    date_since = "2019-1-1"

    tweets = tw.Cursor(api.search,
                        q=search,
                        lang="en",
                        since=date_since).items(1000)
    
    results = []

    for tweet in tweets:
        single_tweet = {"source": "Twitter", "date": "", "text": ""}
        cleaned_tweet = re.sub(r"http\S+", "", tweet.text)
        single_tweet["date"] = str(tweet.created_at)[:10]
        single_tweet["text"] = cleaned_tweet
        results.append(single_tweet)
    
    with open("temp.json", "w") as output_file:
        json.dump(results, output_file)
