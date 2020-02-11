import urllib3 
import json
from bs4 import BeautifulSoup
print("Crawling starts!")

# url = "www.baidu.com"
# http = urllib3.PoolManager()
# response1 = http.request('GET', url)

# with open("./result.txt", 'wb') as result:
# 	result.write(response1.data)

soup = BeautifulSoup(open("./testpage.html"), features='lxml')
for child in soup.html.descendants:
	print(child)

