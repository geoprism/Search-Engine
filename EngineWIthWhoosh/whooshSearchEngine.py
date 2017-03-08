from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
from bs4 import BeautifulSoup
import os.path
from pathlib import Path
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


    def makeSearch(self, qy: str):
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
                #print(results[i].highlights("content", text= body ))

                temp["description"] = results[i].highlights("content", text= body )
                temp["title"] = results[i]["title"]
                total.append(temp)

        #print(total)
        return total

    def createIndex(self):
        """ creates the index """
        writer = self.ix.writer()
        files = self.fileSearch(Path('WEBPAGES_RAW'))
        json_book = json.load(open("WEBPAGES_RAW/bookkeeping.json"))
        for filename in files:
            #print("Indexing: ", str(filename)[16:])
            #print(json_book[str(filename)[16:]])
            writer.add_document(path = str(filename)[13:], content = self.grabsContent(str(filename)), title = self.grabTitle(str(filename)), url = json_book[str(filename)[13:]])
        writer.commit()


    def grabTitle(self, path: str):
        """ grabs title from html"""
        title = path
        f = open(path,'r', encoding="latin-1")
        soup = BeautifulSoup(f, 'lxml')
        temp = soup.find('title')
        if temp != None and temp.text != "":
            title = temp.text
        return title

    def grabsContent(self, path: str):
        """Grabs the content from one document, weights h1,h2,h3,title, strong tags appropriately
           Returns a string
        """
        f = open(path,'r', encoding="latin-1")
        soup = BeautifulSoup(f, 'lxml')
        body = soup.text

        # h1 = " "
        # h2 = " "
        # h3 = " "
        # strong = " "
        # title = " "
        # for words in soup.find_all('h1'):
        #     h1 += ' '.join([words.text, " "])
        # for words in soup.find_all('h2'):
        #     h2 += ' '.join([words.text, " "])
        # for words in soup.find_all('h3'):
        #     h3 += ' '.join([words.text, " "])
        # for words in soup.find_all('strong'):
        #     strong += ' '.join([words.text, " "])
        # for words in soup.find_all('title'):
        #     title += ' '.join([words.text, " "])
        #
        # body += (h1*3) + (h2*2) + (title*2) + h3 + strong #assigns weights to specific tags
        return body

    def fileSearch(self, path: Path):
        """Goes through CORPUS, adds each file that needs to be indexed"""
        filesToIndex = [];
        for directory in path.iterdir():
            try:
                if(directory.is_dir()):
                    for item in directory.iterdir():
                        filesToIndex.append(item)
            except:
                print("Error while adding files to index")
        return filesToIndex

if __name__ == '__main__':
    test = whooshIndexer()
    #test.createIndex()
    q = ""
    while q.lower() != "quit":
        q = input("Query: ")
        if q.lower() != "quit":
            test.makeSearch(q)

































#ignore
