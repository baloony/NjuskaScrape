
class Oglas(object): # jbg neznam kak se to zove na eng :D
    def __init__(self, pid, title, price):
        self.id = pid
        self.title = title
        self.price = price

    def __str__(self):
        return "ID: {}, Title: {}, Price: {}".format(self.id, self.title, self.price)


class UrlResultSet(object):
    def __init__(self):
        self.results = []

    def addoglas(self, oglas):
        self.results.append(oglas)


class DB(object):
    def __init__(self):
        self.oglaslist = {}

    def addresultset(self, url, resultset):
        self.oglaslist[url] = resultset

    def printinfo(self):
        for k, v in self.oglaslist.keys():
            print("url: " + k)

        

        

    


db = DB()
urlresults = UrlResultSet()

o1 = Oglas(1, "prvi", 45)
o2 = Oglas(2, "drugi", 46)

print(o1)
print(o2)

urlresults.addoglas(o1)
urlresults.addoglas(o2)

db.addresultset("nekiURL1", urlresults)
print(db.oglaslist.items())


