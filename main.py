#! python3

import requests, bs4, sys, configparser, argparse
import send
import pickle


class Soup(object):
    def __init__(self, url):
        self.r = requests.get(url)
        self.data = r.text
        self.soup = bs4.BeautifulSoup(data, 'lxml')


class Oglas(object):
    def __init__(self, pid, title, price):
        self.id = pid
        self.title = title
        self.price = price

    def __eq__(self, other):
        return self.id == other.id


class UrlResultSet(object):
    def __init__(self):
        self.results = []

    def addOglas(self, oglas):
        self.results.append(oglas)

    def __contains__(self, oglas):
        return oglas in self.results

    def __repr__(self):
        return "Result set with {} items".format(self.results.__len__())


class DB(object):

    def __init__(self):
        self.oglaslist = {}
        sys.setrecursionlimit(9000)

    def addresultset(self, url, resultset):
        self.oglaslist[url] = resultset

    def printinfo(self):
        print(self.oglaslist)

    def save(self):

        with open('db.bin', 'wb') as f:
            pickle.dump(self.oglaslist, f)

    def load(self):
        with open('db.bin', 'rb') as f:
            temp = pickle.load(f)

            self.oglaslist = temp


def main():
    parser = argparse.ArgumentParser(description="Scrape Njuskalo for ads in certain price range")
    parser.add_argument('url',
                        help='URL of the category you would like to get notifications for')
    parser.add_argument('email',
                        help="Your e-mail address on which you want to receive notifications")
    parser.add_argument('minPrice', metavar="minPrice", type=int,
                        help="Minimal price for a category")
    parser.add_argument('maxPrice', metavar="maxPrice", type=int,
                        help="Maximal price for a category")
    args = parser.parse_args()

    urlResult = UrlResultSet()
    db = DB()

    config = configparser.ConfigParser()
    config.read('config.cfg')
    mailParams = config.items('SERVER')  # [smtp server, username, password]

    # Soup should be in class
    r = requests.get(args.url)
    data = r.text
    soup = bs4.BeautifulSoup(data, 'lxml')

    # Creating a new URL with price range

    categoryId = soup.find("input", {"id": "categoryId"})['value']
    newUrl = "http://www.njuskalo.hr/?ctl=browse_ads&sort=new&categoryId=" \
             "{categoryId}&locationId=&locationId_level_0=0&price[min]={priceMin}" \
             "&price[max]={priceMax}".format(categoryId=categoryId, priceMin=args.minPrice, priceMax=args.maxPrice)

    r2 = requests.get(newUrl)
    data2 = r2.text
    soup2 = bs4.BeautifulSoup(data2, 'lxml')

    for link in soup2.find_all('li', class_="EntityList-item--Regular"):
        print("##### " + link.article.h3.a.string + " #####")
        print("ID oglasa je: " + link.article.h3.a.get("name"))
        print("Link: http://www.njuskalo.hr" + link.article.h3.a.get("href"))
        for price in link.find_all(class_="price"):
            print("Cijena je: " + price.text + "\n")
            o = Oglas(link.article.h3.a.get, link.article.h3.a.get("name"), link.article.h3.a.get("href"))
            urlResult.addOglas(o)

    db.addresultset(args.url, urlResult)
    db.printinfo()
    db.save()

    # db2 = DB()
    # db2.load()
main()
