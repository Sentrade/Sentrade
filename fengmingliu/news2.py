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
soup = BeautifulSoup(response1.data, features='lxml')
with open('./htmlcode.txt', 'w', encoding = 'utf-8') as f:
    f.write(soup.prettify())

# parse the text
result = {}
result["title"] = str(soup.title.string)
result["text"]  = ''
for paragraph in soup.find_all(lambda tag: tag.name == 'p' and not tag.attrs):
	result["text"] = result["text"] + str(paragraph.string)

print(soup.find_all())


# dump to json file
with open('./result.json', 'w', encoding = 'utf-8') as result_json:
	json.dump(result, result_json, ensure_ascii=False, indent=4)

