# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 19:58:17 2020

@author: Fengming Liu
"""

import urllib3 
import json
from bs4 import BeautifulSoup
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
    for paragraph in soup.find_all(lambda tag: tag.name == 'p' and (not tag.attrs or {"class": "article__body-text"})):
        text = text + str(paragraph.string)
    if (soup.title):
        title = str(soup.title.string)
    else:
        title = None
    return title, text

def data_to_json(file_basename, data):
    with open("./result/json_{0}.json".format(file_basename), 'w', encoding = 'utf-8') as json_file:	
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def remove_last_dir(url):
    return url[:url.rfind('/')]

def get_sub_links(source, url):
    soup = download_page(url)
    sublinks = []
    if source == "Economist":
        for tag in soup.find_all('a', class_="teaser__link", itemprop="url", target="_self"):
            sublinks.append(remove_last_dir(url) + tag['href'])
    elif source == "Financial_Times":
        for tag in soup.find_all('a', class_="js-teaser-heading-link", attrs={"data-trackable": "heading-link"}, href=re.compile(r"/content/.*")):
            sublinks.append(url + tag['href'])
    elif source == "Yahoo_Finance":
        for tag in soup.find_all('a', href=re.compile(r"{0}/.*".format(url))):
#            sublinks.append(remove_last_dir(url) + tag['href'])
            sublinks.append(tag['href'])
    else:
        pass

    return sublinks

def get_date(source, url=None, soup=None):
    if source == "Economist":
        if (url):
           pattern = re.compile(r'\d\d\d\d/\d\d/\d\d')
           date = pattern.search(url).group()
           [year, month, day] = date.split('/')
           return "{0}-{1}-{2}".format(year, month, day)
        else:
            return None
    elif source == "Financial_Times":
        if (soup):
            pattern = re.compile(r'"dateModified":"\d\d\d\d-\d\d-\d\d')
            date = pattern.search(str(soup.html))
            if date:   
                date = date.group().split('"')[-1]
                return date
            
            pattern = re.compile(r'"datePublished":"\d\d\d\d-\d\d-\d\d')
            date = pattern.search(str(soup.html))
            if date:   
                date = date.group().split('"')[-1]
                return date
            
            return None                
        else:
            return None
    elif source == "Yahoo_Finance":
        if (soup):
            pattern = re.compile(r'datetime="\d\d\d\d-\d\d-\d\d')
            date = pattern.search(str(soup.html))
            if date:   
                date = date.group().split('"')[-1]
                return date
        
        return None
    else:
        pass

########################################################
##################### Main Program #####################
########################################################


#url = "https://finance.yahoo.com/news/mcdonalds-black-executives-sue-over-185057556.html"
#print(get_sub_links("Yahoo_Finance", url))
#soup = download_page(url)
#write_prettified_html("Yahoo", soup)
#print(get_date("Yahoo_Finance", url, soup))
#title, text = get_title_text(soup)


FN_data = pd.DataFrame(columns=["source", "url", "title", "text", "date"])

#sublinks_economist = get_sub_links("Economist", "https://www.economist.com/finance-and-economics")
#for link in sublinks_economist:
#    soup = download_page(link)
#    title, text = get_title_text(soup)
#    FN_data = FN_data.append({"source": "Economist", 
#                              "url": link,
#                              "title": title, 
#                              "text": text, 
#                              "date": get_date("Economist", link, soup)}, ignore_index=True)

#sublinks_FT = get_sub_links("Financial_Times", "https://www.ft.com")
#for link in sublinks_FT:
#    soup = download_page(link)
#    title, text = get_title_text(soup)
#    FN_data = FN_data.append({"source": "Financial_Times", 
#                              "url": link,
#                              "title": title, 
#                              "text": text, 
#                              "date": get_date("Financial_Times", link, soup)}, ignore_index=True)

sublinks_FT = get_sub_links("Yahoo_Finance", "https://finance.yahoo.com/news")
for link in sublinks_FT:
    soup = download_page(link)
    title, text = get_title_text(soup)
    FN_data = FN_data.append({"source": "Yahoo_Finance", 
                              "url": link,
                              "title": title, 
                              "text": text, 
                              "date": get_date("Yahoo_Finance", link, soup)}, ignore_index=True)
