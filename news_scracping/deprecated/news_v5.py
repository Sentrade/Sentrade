# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 19:58:17 2020

@author: Fengming Liu
"""

import urllib3 
import json
import bs4
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

def get_title_text(source, soup):
    text = ''
    if source == "Business_Insider":
        for paragraph in soup.find_all(lambda tag: tag.name == 'p'):
            for ch in paragraph.children:
                if isinstance(ch, bs4.element.NavigableString):
                    text = text + ch
                elif isinstance(ch, bs4.element.Tag):
                    if ch.name == 'a' and ch.string:
                       text = text + ch.string
    else:
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
            sublinks.append(tag['href'])
    elif source == "Business_Insider":
        for tag in soup.find_all('a', href=re.compile(r"{0}/.*-\d\d\d\d-\d*".format("https://www.businessinsider.com"))):
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
    elif source == "Business_Insider":
        if (soup):
            pattern = re.compile(r'"dateModified":"\d\d\d\d-\d\d-\d\d')
            date = pattern.search(str(soup.html))
            if date:   
                date = date.group().split('"')[-1]
                return date
    else:
        pass
    
def get_FNdata(FN_data, source, main_url):
    sublinks = list(set(get_sub_links(source, main_url)))
    for link in sublinks:
        soup = download_page(link)
        title, text = get_title_text(source, soup)
        FN_data = FN_data.append({"source": source, 
                                  "url": link,
                                  "title": title, 
                                  "text": text, 
                                  "date": get_date(source, link, soup)}, ignore_index=True)
    return FN_data
########################################################
##################### Main Program #####################
########################################################

#source = "Business_Insider"
#url = "https://www.businessinsider.com/apple-music-tv-news-subscription-bundle-arrive-2020-2019-11"
##print(get_sub_links("Business_Insider", url))
#soup = download_page(url)
#write_prettified_html(source, soup)
##print(get_date("Yahoo_Finance", url, soup))
#title, text = get_title_text(source, soup)
#print(title)
#print(text)

#FN_data = pd.DataFrame(columns=["source", "url", "title", "text", "date"])
#FN_source = {"Business_Insider": "https://www.businessinsider.com/s?q=Apple&r=US&IR=T"}
#            "Economist": "https://www.economist.com/finance-and-economics", 
#            "Yahoo_Finance": "https://finance.yahoo.com/news"}
#             "Financial_Times": "https://www.ft.com/world/uk"}

#for source, main_url in FN_source.items():
#    FN_data = get_FNdata(FN_data, source, main_url)
#    
FN_data.to_json("./result/FN_data.json", orient='records')