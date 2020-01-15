"""
This package contains sentiment_analysis(filename) function, which takes in the
news.json file and generate a sentiment.json file with updated entries.

e.g.

Original news.json:
[
    {
        "title": "Amazing news of Apple",
        "date": "2019-12-26",
        "text": "Apple is performing amazingly good. Now it's the time to invest.",
        "source": "twitter"
    },
    {
        "title": "Another amazing news of Apple",
        "date": "2019-12-27",
        "text": "Apple is performing amazingly good again! Now it's the time to invest! Great return.",
        "source": "twitter"
    },
    {
        "title": "And another amazing news of Apple",
        "date": "2019-12-30",
        "text": "Apple is performing amazingly good again! Now it's the time to invest! Great return. Invest now.",
        "source": "Business Insider"
    }
]

Generated sentiment.json:
[
    {
        "polarity": 0.7,
        "title": "Amazing news of Apple",
        "text": "Apple is performing amazingly good. Now it's the time to invest.",
        "source": "twitter",
        "subjectivity": 0.6000000000000001,
        "date": "2019-12-26"
    },
    {
        "polarity": 0.9,
        "title": "Another amazing news of Apple",
        "text": "Apple is performing amazingly good again! Now it's the time to invest! Great return.",
        "source": "twitter",
        "subjectivity": 0.675,
        "date": "2019-12-27"
    },
    {
        "polarity": 0.9,
        "title": "And another amazing news of Apple",
        "text": "Apple is performing amazingly good again! Now it's the time to invest! Great return. Invest now.",
        "source": "Business Insider",
        "subjectivity": 0.675,
        "date": "2019-12-30"
    }
]

"""

from textblob import TextBlob
import json
# from social_news import *
# from business_news import *

def sentiment_analysis(filename):

    """
    PREREQUISITE: 
    calling functions from news scraping here to generate json files here
    e.g. scrap_twitter()
    """

    # Open and load the news json file.
    with open(filename) as input_file:
        news = json.load(input_file)

    # Iterate through the news file, add sentiment analysis result to each entry.
    for item in news:
        blob = TextBlob(item["text"])
        # Property "polarity" and "subjectivity" doesn't exist in the original json file entries,
        # they will be added automatically.
        item["polarity"] = blob.sentiment.polarity
        item["subjectivity"] = blob.sentiment.subjectivity
    
    # Write the updated information to the 
    with open("sentiment.json", "w") as output_file:
        json.dump(news, output_file)

if __name__ == "__main__":
    sentiment_analysis("news.json")
