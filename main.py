#! python3

import requests, bs4, json, sys
import send
# sysargv[1] = URL


#class WebData(object):
#	def __init__(self):
#		self.r = requests.get(sys.argv[1])
#		self.soup = bs4.BeautifulSoup(r.text, 'lxml')

class Oglas(object):
	def __init__(self, pid, title, price):
		self.id = pid
		self.title = title
		self.price = price
		super().__init__()

class UrlResultSet(object):
	def __init__(self):
		self.results = []

	def addOglas(self, oglas):
		self.results.append(oglas)

class DB(object):
    def __init__(self):
        self.oglaslist = {}

    def addresultset(self, url, resultset):
        self.oglaslist[url] = resultset

    def printinfo(self):
        for k in self.oglaslist:
            print("url:" + k)

        

        





url = 'http://www.njuskalo.hr/ps4-konzole'
r = requests.get('http://www.njuskalo.hr/ps4-konzole')
data = r.text
soup = bs4.BeautifulSoup(data, 'lxml')
urlResult = UrlResultSet()
db = DB()

for link in soup.find_all('li', class_="EntityList-item--Regular"):

	print("##### " + link.article.h3.a.string + " ##### ")
	print("ID oglasa je: " + link.article.h3.a.get("name"))
	print("Link: http://www.njuskalo.hr" + link.article.h3.a.get("href"))
	for price in link.find_all(class_="price"):
		print("Cijena je: " + price.text + "\n")
		o = Oglas(link.article.h3.a.get, link.article.h3.a.get("name"), link.article.h3.a.get("href"))
		urlResult.addOglas(o)

db.addresultset(url, urlResult)
db.printinfo()

#data = open("data.p", "w")
#data.write(json.dumps(dataList))