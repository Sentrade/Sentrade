# Sentiment Analysis on Financial News

An algo-trading product for faciliating investors on stock trading based on sentiment analyais of relevant financial news.

## Getting Started

To clone it without the lfs, use:
```
export GIT_LFS_SKIP_SMUDGE=1
```

### Installing

Install all required packages use:
```
pip install -r requirements.txt
```

### Data query
To get access to the raw data, call REST API by:
```
api-sentrade.doc.ic.ac.uk/data/<company_name>
```
where company name can be chosen from:
apple, amazon, facebook, google, microsoft, netflix, tesla, uber.
    

## Deployment

To run it on the server and log the output messages, use:
```
nohup python sentrade.py > output.txt &
```

## Built With


* [Tweepy](https://www.tweepy.org/) - A python library for accessing twitter API.
* [TextBlob](https://textblob.readthedocs.io/en/dev/) - Sentiment analysis engine based on [nltk](https://www.nltk.org/).

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

(Alphabetical order --- we are democratic! :wink:)
* **Davide Locatelli** - *User interface development, sentiment analysis* - [LinkedIn](https://www.linkedin.com/in/davide-locatelli-02011998/)
* **Fengming Liu** - *Data filtration, machine learning* - [LinkedIn](https://www.linkedin.com/in/%E4%B8%B0%E9%93%AD-%E5%88%98-a10632118/)
* **Nora Li** - *Financial data scraping, front end design* - [LinkedIn](https://www.linkedin.com/in/longzhen-nora-li-bb8a9312a/)
* **Sara Yin** - *Social media business news scraping* - [LinkedIn](https://www.linkedin.com/in/shaomiao%EF%BC%88sara-y-1a44b7170/)
* **Yiwen Sun** - *Financial data scraping and maintatining* - [LinkedIn](https://www.linkedin.com/in/yiwen-sun-120a9914b/)
* **Ziyou Zhang** - *Group leader, database developmen, data study* - [LinkedIn](https://www.linkedin.com/in/ziyou-zhang/)

## Acknowledgments

* This project is supervised by [Dr Anandha Gopalan](https://www.imperial.ac.uk/people/a.gopalan): a visionary, experienced and helpful mentor.
