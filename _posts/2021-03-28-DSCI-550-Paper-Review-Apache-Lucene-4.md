---
layout: post
title:  "Paper Review: Apache Lucene 4"
author: Yuchen Zhang
categories: project
date:   2021-03-28
tags: ["paper-review"]
---

![myimg](https://www.youtube.com/watch?v=FhonejJcFpc&t=1s)

Today I'm presenting a Paper called [Apache Lucene 4](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.310.1024&rep=rep1&type=pdf) from proceedings of the Sigia 2012 workshop on information retrieval. The following are the script for the YouTube video.

## Related work & background

First a little background, Lucene was originally written by Doug Cutting in 1997 as a side project of learning Java when he was working for a company called Excite. Then after the company went bankrupt, he decided to make Lucene open source.

From the beginning, Lucene supports a variety of query types like fielded terms with boosts, wildcards, fuzzy words using edit distance, proximity searches, and boolean operators. After it was open-sourced, Lucene kept adding features over the years including support for regular expressions, spatial distances, and arbitrary scoring functions.

Related works include Xapian, the Lemur[li:mer] project, the Terrier IR platform, and managing gigabytes for java. All of them are information retrieval systems or full-text search engines.

## What is Lucene

So, what is Lucene? Well, Lucene is a full-text search engine, in fact, a high-performance search engine library written in Java. It has scalable, high-performance indexing. We will discuss this in detail later. It has powerful, accurate, and efficient search algorithms. And it has cross-platform solutions like python library PyLucene or C# implementation Lucene.NET. 

## Why should you care about Lucene?

Well, to understand how the search system works. Obviously, nowadays we have big companies like Google who control the search engine industry, but there's the other end of the spectrum for instance Twitter uses Lucene to do real-time searches over tweets. That's over a billion queries a day back in 2011. 

There's an article back in 2012 titled "DotLucene: Full-Text Search for your intranet or website using 37 lines of code". We can see how easy Lucene can be implemented.

Big 500 companies are still using it (or some variant of Lucene) today! As for our Data Scientists, MongoDB, Apache Solr, and Elasticsearch use it too. As I heard from the internet, even though Apache Lucene has been updated to 8.x.x, some companies are still using 4.x.x. This means that this paper is still relevant today, which is pretty amazing.

Also the high-performance aspect of Lucene. I will discuss it later in the slides. 

Finally, one could leverage its ideas and build your own search engine.

## Information Retrieval (IR)

Lucene is a type of information retreival system like a google search engine. For search engines, we need it to be accurate, fast, and preferably powerful. Obviously, we want it to be accurate. We also want it to be fast because we don't want to wait days to issue a query. We may also want it to be powerful to issue complex quereis like fuzzy, wildcard, or phrase queries. On the right, we can see that Google can also highlight the terms you issued.

To tackle these problems, a simple solution could be matching the exact terms as we did in assignment 1. However, first, it's not powerful even when you use something like regular expressions. Second, it's slow to match the exact term because you have to go through every single document. If you used regular expression, it's even slower. 

Even though re is accurate, it's accurate to a certain degree. You have to consider capitalization, the order of the terms, and fuzzy words like the word pizza with multiple z's, etc.

Lucene overcame these problems by using a key idea called the inverted index. 

## Inverted index

So what is the inverted index? The inverted index is the opposite of the forward index. So forward index lists each document and its corresponding terms while the inverted index lists terms and the corresponding list of documents that have these terms. This results in a higher performance search efficiency.

## Foundations

To begin, we need to extract terms both from documents and queries. Lucene will not only extract the term or token but also many attributes associated with the token such as token position, starting and ending offsets, token length, etc.

Lucene includes many many analysis implementations. And these implementations have their jobs including stemming, stop word removal, creation of n-grams, tagging, etc. All of which we have covered in class.

As you can imagine, having this many things could be very costly. However, Lucene version 4 also leveraged the finite state transducer (FST) package to significantly reduce memory usage.

## Indexing

Move on to indexing. Lucene uses a document model to store all the information. Documents are modeled in Lucene as a flat ordered list of fields with content. The parsing outputs look very similar to Apache Tika. Not only have the extracted content in one of the key-value pairs, but also other attributes depending on their type. Each key-value pair is called a field. A field is either indexed or stored or both. We may want the field to be indexed but not stored. For example, we index a bunch of PDFs but not store them because they are stored elsewhere. We may also want to store a field but not index it. For example, we may only want to query on the content of the PDFs, but not its title. In this case, the title is stored but not indexed.

## Incremental Index Updates

After indexing, we can start searching. However, before searching, we need to talk about scalability. For the search engine to search over hundreds, even millions, billions of documents, it needs some sort of scalability because indexing takes time, a lot of time in fact. 

When adding a new document, Lucene adds the indexed document in memory and stores it in segments. Periodically these in-memory segments are flushed to persistent storage. Also, as you can imagine, having more segments will decrease the performance since indices are spread all over the place and make it costly to find a document. One method is to merge segments to have fewer of them, however, merging is also costly to do. So Lucene will periodically merge them to comprise the whole index.

Document deletions in Lucene 4 have some quirks too. Each deletion is marked as deleted but not actually deleted similar to page deletion in SSD. This mechanic is different from previous versions of Lucene's because the parts containing deletions can be set as immutable and each operation is committed with timestamps. Otherwise, if some segments are mutable, previous versions of Lucene's will actually lock down the segments which will result in a decrease in performance.

Finally, IndexReader class uses Codec API to retrieve and decode index data.

## Codec API

Move on to the Codec API. The Codec API is essentially an API that encodes the index data into files. Additionally, it can also decode the byte data for reading and merge segment data.

The Codec API stores the data into four columns. These four columns are field, term, document, and position. The structured data can be easily retrieved with an imaginary cursor.

The paper also highlights the codec implementation in Lucene 4 which is called "Lucene40". "Lucene40" provides a good tradeoff between index size and coding costs.

There's also a directory API for storing these codecs into a simple file system-like view of persistent storage.

## Searching

Finally, into searching. Lucene uses a Query object instead of just a keyword string to perform queries. This enables programmers to construct more complex queries or to feed them into a query parser. 

Using an object-oriented programming approach also enables more query types. Lucene 4 supports lots of them like wildcard, fuzzy and regular expression queries, etc.

For query evaluation, as said previously, index data is stored in segments, so query evaluation will sequentially go over segments for efficiency. In addition, to just find matches, we also want to sort the results by best match, so it generates a Scorer for each index segment. Finally, a Collector will consume Scorers and do something with these results.

The Similarity class implements a policy for scoring terms and query clauses. This is specifically good for fuzzy searches whereas users may accurately find the results even if they have a typo in the query. We can use edit distance as we learned in class to find the similarities between the fuzzy word and the actual term. It also has implementations like TF-IDF as we learned in class. 

Finally, it also has common search extensions to support easier navigation of search results.

## Conclusion

In conclusion, this paper gave a historic view of Lucene and explained in detail how Lucene works. The paper also highlights some key features in Lucene 4 like immutable segments, new Codecs, more query types, etc.

## Evaluation

Lastly, my takes on this paper. 

First, the paper has a very good structure. Originally, I was going to talk about Lucene chronologically and logically in my own way. However, as I dig into it, I found the structure of the paper was actually pretty good.

The paper has detailed explanations of Lucene.

Interesting ideas on improving performance. I have stated in the beginning how Lucene cares about performance. As we go along, we can see that Lucene contains many little features here and there to improve its efficiency and accuracy. 

Besides its pros, it also has some drawbacks. First too many jargons. I'm always not a fan of jargons. Even though I have to give the authors credits that Lucene was an early project, and it has been developing many versions over the years, explaining it simply was hard. However, I would love to see people discuss amazing ideas in simple sentences.

Obscure and not well-typeset figures. Well, there are three figures in the paper, but the authors only discussed one. The other two are too sophisticated to show off.

Sporadic feature highlights on Lucene in version 4.

And finally, as a complaint, PyLucene, which is a python framework for Lucene, is very hard to install. I tried Mac and Linux, and both of them failed. I wish I could install it easily like every other package so that I can give it a try using python.

## References

- Białecki, A. B., Muir, R. M., & Ingersoll, G. I. (2012, August). Apache Lucene 4. 17–24. [http://www.opensearchlab.otago.ac.nz/FullProceedings.pdf](http://www.opensearchlab.otago.ac.nz/FullProceedings.pdf)
- Brian Will. (2014a, March 5). Text search with Lucene (1 of 2) [Video]. YouTube. [https://www.youtube.com/watch?v=x37B_lCi_gc&t=3s](https://www.youtube.com/watch?v=x37B_lCi_gc&t=3s)
- Brian Will. (2014b, March 5). Text search with Lucene (2 of 2) [Video]. YouTube. [https://www.youtube.com/watch?v=fCK9U3L7c8U&t=36s](https://www.youtube.com/watch?v=fCK9U3L7c8U&t=36s)
- Letecky, D. (2012, November 6). DotLucene: Full-Text Search for Your Intranet or Website using 37 Lines of Code. CodeProject. [https://www.codeproject.com/Articles/9461/DotLucene-Full-Text-Search-for-Your-Intranet-or-We](https://www.codeproject.com/Articles/9461/DotLucene-Full-Text-Search-for-Your-Intranet-or-We)
- Twitter University. (2014, February 26). Apache Lucene: Then & Now [Video]. YouTube. [https://www.youtube.com/watch?v=5444z-L2V2A&t=115s](https://www.youtube.com/watch?v=5444z-L2V2A&t=115s)