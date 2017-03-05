import indexBuilder
from whoosh.analysis import StemmingAnalyzer
import math


class Query:
    def __init__(self):
        self.indexB = indexBuilder.IndexBuilder()
        self.invertedIndex = self.indexB.buildInvertedIndex()
        self.corpusCount = 1+self.indexB.getCorpusCount()  #make sure corpus count is always +1, so idf is never 0


    def calcQueryVector(self):
        """ask for input and calulate query vector"""
        query = input("Query: ");
        ana = StemmingAnalyzer() ### lowercases, stems, ignores stopwords
        tokens = [token.text for token in ana(query)]

        queryVector = {}
        for token in tokens:
            if token in self.invertedIndex.keys():
                if token in queryVector.keys():
                    queryVector[token]+=1;
                else:
                    queryVector[token] = 1;

        return self.normalizeQueryVector(queryVector);

    def normalizeQueryVector(self, queryVector: dict):
        """ Normalize query vector, using tf-idf """
        magnitude = 0.0
        for word in queryVector.keys():
            queryVector[word] = 1 + math.log10(queryVector[word])  #term frequency
            queryVector[word] *= math.log10(self.corpusCount/len(self.invertedIndex[word])) #inverse document freq
            magnitude += (queryVector[word] ** 2);
        magnitude = math.sqrt(magnitude)
        for word in queryVector.keys():
            queryVector[word] /= magnitude
        return queryVector


    def getResults(self, queryVec: dict):
        """ Get the results that match a term, but later need to rank results """
        result = set()
        for word in queryVec.keys():
            if word in self.invertedIndex:
                result.update(self.invertedIndex[word].keys())
        #print (result)
        #print (self.corpusCount)
        return result

    def rankResults(self, results:set, queryVec: dict):
        """rank the results by comparing cosine similarity, ignoring idf on document vector"""
        rankedResults = {}
        for result in results:
            cosineSim = 0.0
            for word in queryVec.keys():
                if result in self.invertedIndex[word]:
                    cosineSim += queryVec[word]*self.invertedIndex[word][result]
            cosineSim += self.boostScore(result, queryVec.keys())
            rankedResults[result] = cosineSim

        return rankedResults

    def boostScore(self, result: str, words:set ):
        """ boost square proportinal to how many terms found in document """
        found = 0;
        for word in words:
            if result in self.invertedIndex[word]:
                found += 1
        return found/len(words)

    def printIndex(self):
        for key in sorted(self.invertedIndex.keys()):
            print ("{:15} {}".format(key, self.invertedIndex[key]))


    def printInRankedOrder(self, rankedRes:dict):
        """ print rankedResults based on highest cosineSim """
        i = 0
        for docid, count in sorted(rankedRes.items(), key=lambda x: (x[1],x[0]), reverse=True):
            print ("{:15} {}".format(docid, count))
            i +=1
            if i == 10:
                return










if __name__ == '__main__':
    test = Query()
    while True:
        queryVec = test.calcQueryVector()
        results = test.getResults(queryVec)
        ranked = test.rankResults(results, queryVec)
        test.printInRankedOrder(ranked)
