import urllib3
import shutil

http = urllib3.PoolManager()
url = 'https://ia803103.us.archive.org/7/items/archiveteam-twitter-stream-2019-08/twitter_stream_2019_09_19.tar'
with http.request('GET', url, preload_content=False) as response, open('./2019_09_19.tar', 'wb') as out_file:
	shutil.copyfileobj(response, out_file)
