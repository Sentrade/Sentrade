#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Davide Locatelli, Ziyou Zhang"
__status__ = "Prototype"

import re, string
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')
text = twitter_samples.strings('tweets.20150430-223406.json')
tweet_tokens = twitter_samples.tokenized('positive_tweets.json')

def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word,pos))
    return lemmatized_sentence

def remove_noise(tweet_tokens, stop_words = ()):
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-".&+#]|[!*\(\),]|)'\
        '(?:%[0-9a-fA-F][0-9a-fA-F]))+','',token)
        token = re.sub("(@[A-Za-z0-9_]})","",token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        
        lemmatizer = WordNetLemmatizer()
        token - lemmatizer.lemmatize(token,pos)

        if len(token)>0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
            return cleaned_tokens