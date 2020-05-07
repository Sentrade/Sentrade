from textblob import TextBlob

__author__ = "Davide Locatelli"

def get_blob(text):

    blob = TextBlob(text)
    return blob.sentiment.polarity

def get_score(text):

    blob = get_blob(text) + 1
    blob /= 2
    blob *= 100

    return blob