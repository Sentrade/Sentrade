import urllib3 
import json
import sys
from bs4 import BeautifulSoup
print("Crawling starts!")

import warnings
warnings.filterwarnings("ignore")

# download the webpage
url = sys.argv[1]
print("Crawl the url:", url)
http = urllib3.PoolManager()
response1 = http.request('GET', url)
print("Status of the response:", response1.status)

# encapsulate the reponse in a soup
soup = BeautifulSoup(response1.data, features='lxml')
for tag in soup.find_all('a', href=True):
	if tag['href'].endswith(tuple([".h", ".cpp", ".pdf", ".h", ".dat", ".txt"])):
		link = "{0}/{1}".format(url, tag['href'])
		try:
			filename = "./result/{0}".format(tag['href'])		
			print(filename)
			result_file = open(filename, 'wb')
		except:
			print(tag['href'], " can't be created!")
		else:
			response2 = http.request('GET', link)
			print(link)
			result_file.write(response2.data)
			result_file.close()



