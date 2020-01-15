import json
from twython import Twython
import pandas as pd
:json stores
: pandas

def getTweetInterface():
	credentials = {}
	credentials['CONSUMER_KEY'] = 'N1naTf3Iy8IbrwTcGWXLzOcuI'
	credentials['CONSUMER_SECRET'] = 'zZq4yjhTuihFucyfxtJpelGO66RVv8P8tJNSgdBBHYk9oGmQLF'
	credentials['ACCESS_TOKEN'] = '1212877716233408512-ndWwAwCCzF48k2MXdNULnCo5kWjtzo'
	credentials['ACCESS_SECRET'] = 'jm2Zvg9J2pyq2bKRU5CaUfYBdKI6fRvvsEOk2FuADOOR7'

	python_tweets = Twython(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
	return python_tweets
:return getTweetInterface

def queryCompany(tweetInterface, company):
	query = {'q': company,
        'result_type': 'popular',
        'count': 10,
        'lang': 'en',
        }
:param tweetInterface: this is a first param
:param company: this is a second param
:returns queryCompany
:raises key Error:

	dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
	for status in tweetInterface.search(**query)['statuses']:
	    dict_['user'].append(status['user']['screen_name'])
	    dict_['date'].append(status['created_at'])
	    dict_['text'].append(status['text'])
	    dict_['favorite_count'].append(status['favorite_count'])

	# Structure data in a pandas DataFrame for easier manipulation
	df = pd.DataFrame(dict_)
	df.sort_values(by='favorite_count', inplace=True, ascending=False)
	return df

tweet = getTweetInterface()
df = queryCompany(tweet, 'apple')
print(df.head(10))
