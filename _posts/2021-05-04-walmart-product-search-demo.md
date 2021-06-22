---
layout: post
title:  "Walmart Product Search Project with Demo"
date:   2021-05-04
category: project
author: 
    - "Yuchen Zhang"
    - "Zian Fan"
tags: ["backend", "frontend", "search", "flask"]
---

{% figure walmart-search-demo png 'Walmart Search Demo' %}

- [Check out demo here](#check-out-demo-here)
- [Scripts](#scripts)
  - [Where we stored the data](#where-we-stored-the-data)
  - [Demo](#demo)

## Check out demo [here](https://www.dsci-551-project-walmart-demo.ml)

I'm using a new domain name from freenom that will support for an year. I deployed the website on AWS ec2.

## Scripts

### Where we stored the data

We eventually used MongoDB. It's worth mentioning that we tried MySQL and Cassandra. However, our data is kinda tedious to be stored tabularly. Even though it can, it takes a very long time to insert and the final database file is enormous, so it's not very portable for us to implement into our website. Regarding to Cassandra, the problem was we wanted to store our data on the cloud and at that time professor conveniently put up the github pro information so that we expand our storage with $200 credits mongodb offered. Finally, it's easier to index with MongoDB using Lucene. Coincidentally, I also did a paper review about Lucene in another class. Lucene is sort of the foundation of Apache Solr and Elasticsearch, and it did a really good job for us to implement its search functionality into our UI.

### Demo

I will jump right into the demo of our project. So our goal was to just rebuild the search functionality from the online shopping websites like Walmart or Amazon.

You can see there's a title says search a product in our database. And we said that the database uses 6000 pages using Walmart API, then we used spark to filter out not in stock and not available online products beforehand.

The next paragraph is live updated. So, currently we have 344304 products on MongoDB. This is just counting how many documents in our database. It also says we have 3979 distinct categories. The walmart api actually has unique identifiers for each category. So this is counting unique number of those identifiers. Then, finally, it calculates the average number of reviews each product has.

Then we have a big search bar for searching items and a list of filtering options. Each filtering option has number of products our database has. So before searching, it counts how many products fall into each category.

So if we type search query like "Apple" and click on the search button. First we can immediately see that it gives us what the top categories of the search results are and it also gives how many products fall into each category. For very long category paths, it also truncates them to smaller path.

Then, we can see that filtering options will update number of products each filter contains. These counts will change depending on your search query. So if we click on Clearance, we can see there are actually two items left for the search results.

Speaking of searching, our search index is created around brand name, product name, short description and long description. After index was created, we can perform full-text search on these fields. 

So, the word "apple" with clearance filter will give us these two results and we can see that the word apple is in both the product name and their descriptions.

For the search results, we can see that we have brand name, product name, its star rating based on their actually ratings, number of reviews it has, of course its description. Also if the product is in sale, it will have its MSRP, and its sale price. Additionally, we have two types of shipping rates for each product. Finally, we can also view the product on Walmart.com if it has the product url given. Unfortunately, we supposed to have all the product links at the beginning of the semester when we scraped the data. However, Walmart has changed some of the fields during the semester, so lots of products doesn't have their link anymore. Anyway, if they do, you can redirect to the walmart.com and see the details.

So if I click on this link, it will redirect me to the exact same product on walmart.com. You can see that the information is the same as our search results.