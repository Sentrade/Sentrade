__author__ = "Davide Locatelli, Ziyou Zhang"
__status__ = "Development"

from bert_predict import predict_score
from pymongo import MongoClient
import dash_html_components.Time

def bert_sentiment_database(company_name):

    client = MongoClient('mongodb://admin:sentrade@45.76.133.175:27017')
    twitter_db = client.twitter_data

    count = 0
    all_news = twitter_db[company_name].find()
    
    for news in all_news:
        score = predict_score(news["processed_text"])
        print(f'score {score}')
        bert_polarity = {"$set": {"bert_polarity": score}}
        twitter_db["company_name"].update_one(news, bert_polarity)
        count += 1
        print(f'count {count}')
        if (count >= 150000):
            break

    client.close()

if __name__ == "__main__":
    bert_sentiment_database("tesla")