#! python3

import requests, bs4, json, sys


url = 'http://www.njuskalo.hr/ps4-konzole'
r = requests.get('http://www.njuskalo.hr/ps4-konzole')
data = r.text
soup = bs4.BeautifulSoup(data, 'lxml')
dataList = {}

for link in soup.find_all('li', class_="EntityList-item--Regular"):
	print("##### " + link.article.h3.a.string + " ##### ")
	print("ID oglasa je: " + link.article.h3.a.get("name"))
	print("Link: http://www.njuskalo.hr" + link.article.h3.a.get("href"))
	for price in link.find_all(class_="price"):
		print("Cijena je: " + price.text + "\n")
		dataList[url] = {
			'title': link.article.h3.a.string, 
			'id': link.article.h3.a.get("name"),
			'price': price.text
			}

print(dataList)
#data = open("data.p", "w")
#data.write(json.dumps(dataList))