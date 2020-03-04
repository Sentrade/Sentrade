import json
from twython import Twython
import pandas as pd

companyName= 'apple'


def getTweetInterface():
	""
	Function that uses credentials obtained from Twitter developer account to establish a connection to Twitter public API using the Twython Library.

	:returns: Twython interface for later quueries
	""

	credentials = {}
	credentials['CONSUMER_KEY'] = 'N1naTf3Iy8IbrwTcGWXLzOcuI'
	credentials['CONSUMER_SECRET'] = 'zZq4yjhTuihFucyfxtJpelGO66RVv8P8tJNSgdBBHYk9oGmQLF'

	python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
	return python_tweets


def queryCompany(interface, companyName):
	"""
	Function that returns a Panda dataframe containing Tweets related to a given companyName.

	:param interface: Twython interface to be queries
	:param companyName: name of the company
	:returns: panda dataframe containing Tweets
	"""
	query = {'q': company,
        'result_type': 'popular',
        'count': 10,
        'lang': 'en',
        }

	dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
	for status in tweetInterface.search(**query)['statuses']:
	    dict_['user'].append(status['user']['screen_name'])
	    dict_['date'].append(status['created_at'])
	    dict_['text'].append(status['text'])
	    dict_['favorite_count'].append(status['favorite_count'])
	""
        Structure data in a pandas DataFrame for easier manipulation
	""
	
	df = pd.DataFrame(dict_)
	df.sort_values(by='favorite_count', inplace=True, ascending=False)
	return df

def main():
	""
	Main fnction of this program.
	""
	interface = getTweetInterface()
	df = queryCompanyNews(interface, companyName)
	df.sort_values(by='favorite_cont', inplace=True, ascending=False)
	df.head(20)
