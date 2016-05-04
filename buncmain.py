#! python3

import requests, bs4, json, sys
from BClasses import *

# sysargv[1] = URL


class WebData(object):
	def __init__(self):
		self.r = requests.get(sys.argv[1])
		self.soup = bs4.BeautifulSoup(r.text, 'lxml')



r = requests.get('http://www.njuskalo.hr/ps4-konzole')
data = r.text
soup = bs4.BeautifulSoup(data, 'lxml')
db = DB() # ovo je novo


for link in soup.find_all('li', class_="EntityList-item--Regular"):
	print("##### " + link.article.h3.a.string + " ##### ")
	print("ID oglasa je: " + link.article.h3.a.get("name"))
	print("Link: http://www.njuskalo.hr" + link.article.h3.a.get("href"))
	resSet = UrlResultSet() # ovo je novo
	for price in link.find_all(class_="price"):
		print("Cijena je: " + price.text + "\n")


                # nesto tipa
                # o = Oglas(id, i jos svasta)
                #resSet.append(o)
                

        #db.append(url, resSet)


data = open("data.p", "w")
data.write(json.dumps(dataList))
