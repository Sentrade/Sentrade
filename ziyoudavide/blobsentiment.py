#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Davide Locatelli, Ziyou Zhang"
__status__ = "Prototype"

import json
import spacy
from textblob import TextBlob

company = "apple"

def is_org(news,company):
    """
    Function to check if a company is named in a piece of news

    :param news: the news being checked (in JSON format)
    :param company: the name of the company (lowercase)
    :returns: true if the company is named, false otherwise
    """
    nlp = spacy.load("en_core_web_sm") #create a spaCy Language object
    doc = nlp(news["text"]) #select text of the news
    for t in doc.ents:
        if t.lower_ == company: #if company name is called
            if t.label_ == "ORG": #check they actually mean the company
                return True
    return False

def blob_analyse(inputfile,outputfile):
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

if __name__ == "__main__":
    blob_analyse("newsorg.json", "blob_sent.json")
