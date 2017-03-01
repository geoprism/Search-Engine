from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from pathlib import Path
import re
import math

class IndexBuilder:
    def __init__(self):
        self.corpusCount = 0

    def storeWordPosition(self, aFile: Path):
        """Stores the word and the position of that word(doing this for query terms) in a single file
           Ex. {word : [normalized term freq], word2:[normalized term freq], ..}
        """
        stopset = set(stopwords.words('english'))
        stopset.update({"title", "body", "strong"})
        stemmer = PorterStemmer()
        corpi = aFile.open( encoding='latin-1')
        f = corpi.read()
        ###leaving out stemming for now, because not sure how querying will work if i stem.
        tokens = [token for token in word_tokenize(str(f).lower()) if token not in stopset and re.match("^[a-z].+[a-z]$", token) ]
        print("Indexing: ", str(aFile))

        wordPosition = {}
        for token in tokens:
            if token in wordPosition.keys():
                wordPosition[token]+=1
            else:
                wordPosition[token] = 1

        ###weighting for h1,h2,h3,strong,b,title tags for now (boosting tf score)
        # soup = BeautifulSoup(f, 'lxml')
        # for words in soup.find_all('h1'):
        #     important = [token for token in word_tokenize(str(words.text).lower()) if token not in stopset and re.match("^[a-z].+[a-z]$", token) ]
        #     for token in important:
        #         wordPosition[token]+=3


        return self.normalize(wordPosition)

    def normalize(self, wordPosition: dict):  ###for some reason, not normalizing leads to closer scores with lucene
        """Normalize frequencies """
        magnitude = 0.0
        for word in wordPosition.keys():
            wordPosition[word] = 1 + math.log10(wordPosition[word])
        #     magnitude += wordPosition[word] ** 2;
        # magnitude = math.sqrt(magnitude)
        # for word in wordPosition.keys():
        #     wordPosition[word] /= magnitude
        return wordPosition

    def storeDocToWord(self):
        """ {docID: {word: [normalized tf],...}, ...} """
        testData = input("Where is your test data: ")
        files = self.fileSearch(Path(testData))
        total = {}
        for filename in files:
            total[str(filename)[16:]] = self.storeWordPosition(filename)
        return total

    def buildInvertedIndex(self):
        docToWords = self.storeDocToWord()
        invertedIndex = {}
        for filename in docToWords.keys():
            for word in docToWords[filename].keys():
                if word in invertedIndex.keys():
                    invertedIndex[word].update({filename: docToWords[filename][word]})
                else:
                    invertedIndex[word] = {filename: docToWords[filename][word]}
        return invertedIndex


    def fileSearch(self, path: Path):
        """Goes through CORPUS, adds each file that needs to be indexed"""
        filesToIndex = [];
        for directory in path.iterdir():
            try:
                if(directory.is_dir()):
                    for item in directory.iterdir():
                        filesToIndex.append(item)
                        self.corpusCount+=1
            except:
                print("Error while adding files to index")
        return filesToIndex

    def getCorpusCount(self):
        return self.corpusCount


import sys

def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


if __name__ == '__main__':
    test = IndexBuilder()
    x = test.buildInvertedIndex()
    print(get_size(x))
