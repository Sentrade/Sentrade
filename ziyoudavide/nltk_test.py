#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Davide Locatelli, Ziyou Zhang"
__status__ = "Prototype"

import re, string, random
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

def remove_noise(tweet_tokens, stop_words = ()):
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token
    
def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

if __name__ == "__main__":
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')

    text = twitter_samples.strings('tweets.20150430-223406.json')
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')

    stop_words = stopwords.words('english')

    positive_tweets_tokens = twitter_samples.tokenized('positive_tweets.json')
    positive_cleaned_tokens_list = []

    negative_tweets_tokens = twitter_samples.tokenized('negative_tweets.json')
    negative_cleaned_tokens_list = []

    for tokens in positive_tweets_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens,stop_words))

    for tokens in negative_tweets_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens,stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)
    freq_dist_pos = FreqDist(all_pos_words)

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive") for tweet_dict in positive_tokens_for_model]
    negative_dataset = [(tweet_dict, "Negative") for tweet_dict in negative_tokens_for_model]
    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)
    train_data = dataset[:7000]
    test_data = dataset[7000:]

    classifier = NaiveBayesClassifier.train(train_data)

    custom_tweet = "Apple shares were all over the place Tuesday.After announcing two new iPhones, a new Apple Pay payment system, and Apple Watch, Apple shares gained as much as 4.5% and lost as much as 2.2% in a volatile day that saw more than 170 million shares change hands.On Tuesday, Apple announced two new phones, iPhone 6 and iPhone 6 Plus, which will be available to preorder on Sept. 12.Apple also announced a new mobile-payment system, Apple Pay. The company said itThe company has credit-card agreements for Apple Pay with American Express, MasterCard, and Visa.Apple also announced Apple Watch, which sent shares of the company off their best levels. Apple watch will be available in early 2015.You can read BI's wall-to-wall coverage of Apple's announcements over at SAI."
    custom_tokens = remove_noise(word_tokenize(custom_tweet))
    print(classifier.classify(dict([token, True] for token in custom_tokens)))
