from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
from bs4 import BeautifulSoup
import os.path
from whoosh.index import create_in
from whoosh import index
from whoosh.qparser import QueryParser
import json

###ADD TITLE, URL TO SCHEMA!!!!

class whooshIndexer:
    def __init__(self):
        self.schema =  Schema( path = ID(stored = True),
                               content = TEXT(analyzer= StemmingAnalyzer()),
                               title = TEXT(stored = True),
                               url = TEXT(stored = True))
                               ### lowercases, and stems, need to find a way to ignore html tags
        if not os.path.exists("index"):   ##make an index folder if one does not exist
            os.mkdir("index")
            index.create_in("index", self.schema)
        self.ix = index.open_dir("index")         ##index object


    def makeSearch(self, qy):
        """ makes a search """
        qp = QueryParser("content", schema=self.schema)
        q = qp.parse(qy)
        total = []
        with self.ix.searcher() as searcher:
            results = searcher.search(q, limit=20)
            for i in range(results.scored_length()):
                print(results[i]['path'])
                temp = dict()

                #total.append(results[i]['path'])
                temp["url"] = results[i]['url']
                with open("WEBPAGES_RAW/" +  results[i]["path"]) as fileobj:
                    filecontents = fileobj.read()
                    soup = BeautifulSoup(filecontents, 'lxml')
                    body = soup.text
                # print(results[i].highlights("content", text= body ))

                temp["description"] = results[i].highlights("content", text= body)
                temp["title"] = results[i]["title"]
                total.append(temp)

        print(total)
        return total
if __name__ == '__main__':
    test = whooshIndexer()
    #test.createIndex()
    q = ""
    while q.lower() != "quit":
        q = input("Query: ")
        if q.lower() != "quit":
            test.makeSearch(q)
