#! python3

import requests, bs4, json, sys, configparser
import send
# sysargv[] = URL, email, priceRange(1000 2000)

class Oglas(object):
	def __init__(self, pid, title, price):
		self.id = pid
		self.title = title
		self.price = price

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


config = configparser.ConfigParser()
config.read('config.cfg')
mailParams = config.items('SERVER')  # [smtp server, username, password]

url = sys.argv[1]
email = sys.argv[2]
priceRange = sys.argv[3:]

r = requests.get(url)
data = r.text
soup = bs4.BeautifulSoup(data, 'lxml')

#  Construct a new URL - new URL forms when using the price range -> have to extract CategoryID from previous
categoryId = soup.find("input", {"id": "categoryId"})['value']
newUrl = "http://www.njuskalo.hr/?ctl=browse_ads&sort=new&categoryId={categoryId}&locationId=&locationId_level_0=0&price[min]={priceMin}&price[max]={priceMax}".format(categoryId = categoryId, priceMin = priceRange[0], priceMax = priceRange[1])

print(newUrl)

urlResult = UrlResultSet()
db = DB()

for link in soup.find_all('li', class_="EntityList-item--Regular"):

	print("##### " + link.article.h3.a.string + " #####")
	print("ID oglasa je: " + link.article.h3.a.get("name"))
	print("Link: http://www.njuskalo.hr" + link.article.h3.a.get("href"))
	for price in link.find_all(class_="price"):
		print("Cijena je: " + price.text + "\n")
		o = Oglas(link.article.h3.a.get, link.article.h3.a.get("name"), link.article.h3.a.get("href"))
		urlResult.addOglas(o)

db.addresultset(url, urlResult)
db.printinfo()
