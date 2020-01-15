import urllib3 
import json
import sys
from bs4 import BeautifulSoup
import json
import unicodedata
print("Crawling starts!")

import warnings
warnings.filterwarnings("ignore")

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def parse(soup):
	divs = soup.find_all("div")
	return divs
	# for div in divs:
	#     # 一些中间变量
	#     gold = div.find('span', title = re.compile('gold'))
	#     silver = div.find('span', title = re.compile('silver'))
	#     bronze = div.find('span', title = re.compile('bronze'))
	#     tags = div.find('div', class_ = 'summary').find_all('div')[1].find_all('a')

	#     # 用生成器输出字典
	#     yield {
	#     # 这部分每一条都有代表性
	#     'title': div.h3.a.text,
	#     'url': self.baseurl + div.h3.a.get('href'),
	#     'answer': div.find('div', class_ = re.compile('status')).strong.text,
	#     'view': div.find('div', class_ = 'views ').text[: -7].strip(),
	#     'gold': gold.find('span', class_ = 'badgecount').text if gold else 0,
	#     'tagnames': [tag.text for tag in tags],

	#     # 下面的从知识的角度上讲都和上面一样
	#     'vote': div.find('span', class_ = 'vote-count-post ').strong.text,
	#     'time': div.find('div', class_ = 'user-action-time').span.get('title'),
	#     'duration': div.find('div', class_ = 'user-action-time').span.text,
	#     'username': div.find('div', class_ = 'user-details').a.text,
	#     'userurl': self.baseurl + div.find('div', class_ = 'user-gravatar32').a.get('href'),
	#     'reputation': div.find('span', class_ = 'reputation-score').text,
	#     'silver': silver.find('span', class_ = 'badgecount').text if silver else 0,
	#     'bronze': bronze.find('span', class_ = 'badgecount').text if bronze else 0,
	#     'tagurls': [self.baseurl + tag.get('href') for tag in tags]
	#     }

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

# items = list(parse(soup))
# s = json.dumps(list(items))

# with open('./result.txt', 'w', encoding = 'utf-8') as f:
#     f.write(soup.prettify())


