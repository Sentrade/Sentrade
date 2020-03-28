#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Davide Locatelli"
__status__ = "Development"

from bert import get_score
from pytorch_pretrained_bert.modeling import BertForSequenceClassification
import argparse
from pathlib import Path
import datetime
import os

def predict_score(sentence):

    model_path = './models/classifier_model/sentiment/'
    model = BertForSequenceClassification.from_pretrained(model_path, num_labels=3,cache_dir=None)

    result = get_score(sentence,model)
    scores = result['sentiment_score']

    total_score = 0
    total = 0
    for score in scores:

        total_score += score
        total += 1

    total_score = total_score / total
    return total_score

if __name__ == "__main__":
    sentence = "Euronext had given an indicative price of 58.70 euros per share for Prosus, implying a market value of 95.3 billion euros ($105 billion)."
    print(predict_score(sentence))