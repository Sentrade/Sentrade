import urllib3 
import json
import sys
from bs4 import BeautifulSoup
import json
import unicodedata
import re
print("Crawling starts!")

import warnings
warnings.filterwarnings("ignore")

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def no_attr(tag):
	return not tag.has_attr("class")

# download the webpage
url = remove_control_characters(sys.argv[1])
print("Crawl the url:", url)
http = urllib3.PoolManager()
response1 = http.request('GET', url)
print("Status of the response:", response1.status)

# parse the text
soup = BeautifulSoup(response1.data, features='lxml')
with open('./htmlcode.txt', 'w', encoding = 'utf-8') as f:
    f.write(soup.prettify())

f = open('./result.txt', 'w', encoding = 'utf-8')
f.write(str(soup.title) + '\n')
for paragraph in soup.find_all(lambda tag: tag.name == 'p' and not tag.attrs):
	f.write(str(paragraph) + '\n')
f.close()

