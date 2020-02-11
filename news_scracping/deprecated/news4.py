import urllib3 
import json
import sys
from bs4 import BeautifulSoup
import json
import unicodedata
import re
import pandas as pd
print("Crawling starts!")

import warnings
warnings.filterwarnings("ignore")

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def download_page(url):
	print("Crawl the url:", url)
	url = remove_control_characters(url)
	response = urllib3.PoolManager().request('GET', url)
	print("Status of the response:", response.status)
	return BeautifulSoup(response.data, features='lxml')

def write_prettified_html(file_basename, soup):
	with open("./result/html_{0}.txt".format(file_basename), 'w', encoding = 'utf-8') as f:
	    f.write(soup.prettify())

def get_title_text(soup):
	text = ''
	for paragraph in soup.find_all(lambda tag: tag.name == 'p' and not tag.attrs):
		text = text + str(paragraph.string)
	return str(soup.title.string), text

def data_to_json(file_basename, data):
	with open("./result/json_{0}.json".format(file_basename), 'w', encoding = 'utf-8') as json_file:
		json.dump(data, json_file, ensure_ascii=False, indent=4)

def remove_last_dir(url):
	return url[:url.rfind('/')]

def get_sub_links(source, url):
	soup = download_page(url)

	sublinks = []
	if source == "Economist":
		for tag in soup.find_all('a', class_="teaser__link", 
									  itemprop="url", 
									  target="_self"):
			sublinks.append(remove_last_dir(url) + tag['href'])
	elif source == "Financial_Times":
		for tag in soup.find_all('a', class_="js-teaser-heading-link", 
									  attrs={"data-trackable": "heading-link"},
									  href=re.compile(r"/content/.*")):
			sublinks.append(url + tag['href'])
	elif source == "Yahoo_Finance":
		for tag in soup.find_all('a', href=re.compile(r"^/news/.*")):
			sublinks.append(remove_last_dir(url) + tag['href'])

	return sublinks

# write_prettified_html("Yahoo_Finance", download_page("https://finance.yahoo.com/news"))
# print(get_sub_links("Yahoo_Finance", "https://finance.yahoo.com/news"))

FN_data = pd.DataFrame(columns=["source", "url", "title", "text", "date"])
sublinks_economist = get_sub_links("Economist", "https://www.economist.com/finance-and-economics")
# sublinks_FT = get_sub_links("Financial_Times", "https://www.ft.com")

for link in sublinks_economist:
	soup = download_page(link)
	title, text = get_title_text(soup)
	FN_data.append({"source": "Economist", "url": link,
					"title": title, "text": text, "date": None})
