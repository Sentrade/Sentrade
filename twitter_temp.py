import tweepy as tw
import pandas as pd
import json
import re

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
                       since=date_since).items(10000)

# with open("temp.json", "w") as output_file:
#     for tweet in tweets:   
#         json.dump(tweet._json, output_file)

for tweet in tweets:
    cleaned_tweet = re.sub(r"http\S+", "", tweet.text)
    print(cleaned_tweet)