# Search-Engine
Built from scratch with python and good intentions. oh, and scored on tf-idf...

Overall one of my more satisfying projects. I have always been curious how search engine
are implementing, I use one everyday, so they are kind of a big deal :). Plans to
implement a search engine with Whoosh and build an interface. Enjoy!

##References
Most of the algorithms and methodologies are easily found online. A simple google search should do... ;)
Most of the course follows the teaching of Professor Christopher Mannings: http://nlp.stanford.edu/manning/
He teaches CS276 at Stanford and a majority of his lectures are available online.
I found these resources most helpful when building my engine:
http://web.stanford.edu/class/cs276/
Cosine scoring: https://www.youtube.com/watch?v=E3shpvJUZ84&t=423s

Compared my ranked results with Apache Lucene: http://lucene.apache.org/core/

This project should be doable for some one who understands python and basic computing




##My Thoughts

**Test data:** static html pages that I crawled through uci.ics.edu domain

**Stemming/stopwards:** For stemming I used NLTK’s porter stemmer. For stopwords I used NLTK.corpus stopwords and added a few of my own. For example, “strong” would accidently be passed through as a token, which was really the html tag “<strong>”.

**Tokenizer:** For tokenizing I used NLTK’s word_tokenizer, I made sure every word was lowercase and matched the regular expression: "^[a-z].+[a-z]$". In laymen terms, this made sure that every token started and ended with a lowercase character and was at least length  3. This prevented strings such as “h3” or *<b>*, also prevented words with length 2 from entering the index(even though the stopwords would handle this). My tokenizer has very strict rules, plans to allow all alphanumeric characters in the next iteration.

**Indexing:** Indexing was pretty straightforward. Essentially I would take each document and map each unique term and their frequencies. For example, my base index would look like this:
{document1: {word1: n}, {word2: n}, …}.  My base index would be able to map each word inside a specific document. The next step was to transform my intermediary index into my final inverted index, which looked like: {word1: {{document1: n},….}, word2: {{document2:n},…}}. This would map every word to a document and find their occurrences.

**Scoring:** For scoring I would be using the tf-idf scoring standard. Where term frequency could be calculated by (1+log(freq)), which would be multiplied by the idf: log(corpus count/ docs found). Initially, my inverted index stored the frequency of each word, but I would later find it more valuable to store the term frequency score. Further, I found that by not normalizing my term frequency per each document I would find closer results to those produced by Apache Lucene (a search API that handles scoring for you). I purposely only stored the tf score and not the tf*idf score because of complexity issues, and I noticed that slide examples would ignore factoring in the idf score for the document vector. I assumed idf scores would be weighted proportionally to the query vector(assuming the query vector properly calculated tf-idf score, more on this later). In the next iteration, I plan to add idf scoring into my document vector, maybe this will produce results similar to Lucene ☺.

**Querying:** Querying was one of the simpler aspects of this project. I would take a query, run it through our tokenizer and then calculate the full tf*idf score. TF score would be fairly straightforward to calculate with a query. For example query: “machine learning is cool”, would lead to a tf score of [0.5 0.5 0.5 0.5] represented as a vector(normalized). However, this does not include the idf score which is much easier to calculate in the query. Remember, idf is log(collection count/ num of docs found). Collection count is always static, and in this case 1001. Number of doc founds would simply be:  len(inverted_index[word]). On the contrary, calculating idf score for each word for a document vector, would be much harder and time consuming… but I’ll do it before milestone 3.

**Ranking:** The last step in completing a full fledged search engine, actually not full fledged…Google engineers would probably scoff at my implementation. But anyways this is the last step, and probably hardest because there are multiple ways to rank certain documents. For example, a phrase query such as “machine learning”, a user could be expecting results where the words of  the phrase query are always seen next to each other. Intuitively, the user would expect documents related to AI (machine learning synonymous with AI), but what if a document contained the words “machine” and “learning”, although not immediately next to each other. For example, this could be a document talking about learning how to fix a fax machine. My implementation would not be able to decipher between the two/ rank appropriately, further implementation will improve on this, but I hope you get my point. The term for this type of ranking is called Bag of Words model, which I implemented. Mathematically, all that was necessary was to take the cosine similarity, which is the dot product of the query vector and document vector. As mentioned before, I found better results if I excluded normalization and idf scoring in my document vector(more on this in the section below). Lastly, I implemented a boosting function which would take the proportion of the amount of query words found in a document and boost the cosine similarity score. Ex. if a document contained 1 or 2 words from the query, the cosine similarity would be boosted by +0.5. There are probably better ways to do this, but I found by doing so, rankings would be more similar to Lucene. Lasting, I ranked based on descending cosine similarity scores.   

**Obscurities:** Lets talk about the minor obscurities first. Opening files had to be done in “latin-1” encoding which I found weird, because I thought all html/plain text could be opened with “utf-8” encoding. Also I noticed finding the size of an object not to be intuitively easy. Python is not like Java where an int will always be 4 bytes. Probably should have paid more attention in lower division classes, oh well. Now onto the things that really bothered me. Initially, when I normalized by document vectors I noticed that the ranking of documents would be thrown way off. For instance, if I had two documents,  one with just the word “machine learning” and another with “machine learning” x50 times with an additional 1000 random words, the document with just “machine learning” would rank higher. I can see why this is happening, because the tf-idf of the smaller document would suffer a smaller deduction when I divided by the magnitude(normalizing). However, when I cross compared this search againt Lucene, the document with “machine learning” x50, would rank higher, which seems the most logical. Maybe, normalizing is not the best thing to do, especially with some documents in our corpus only containing 20 or so words. But I can see why normalizing would be beneficial, it could show the “importance” of words in a document. You could even argue the document with just “machine learning” is guaranteed to talk only about machine learning because of such a small, concentrated word size, leading to higher relevance/importance.

**Conclusion:** Although daunting at first, I found this project to be extremely satisfying. The ability to make anything searchable is not a power that should be taken lightly. Also, understanding the basics of how search engines works, something I use everyday and will continue to use in the foreseeable future, is quite “cool”. Improvements to come. Mamba out.
