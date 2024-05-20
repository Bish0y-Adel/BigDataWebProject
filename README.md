# BigDataWebProject
this is a simple search engine web project using flask framework for Big data project that represents the result of data in a beautiful way.

requirements:
A mini search engine. The main objective is to employ what students learned in Big Data in a real project. The project consists of three parts

1- Crawler to crawl around 100k news pages starting with a list of 20 news pages as a seed. then get all hyperlinks in the page automatically by code without using scrapy library or any other similar package. some html parsing libraries like beautifulsoup and urllib are allowed.  

2- Using MapReduce algorithm, indexing must be done for all collected data. Inverted index must be constructed where every unique token has a list of indices of documents where it appears

3- Using MapReduce algorithm, implement a search for a single word in the collection (collected news pages) using the inverted index.

4- Using MapReduce algorithm, rank the results using TFIDF scheme.

5- Using MapReduce algorithm, rank the results with PageRank algorithm.
