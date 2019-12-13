#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 19:20:15 2019

@author: libby
"""

import os
import json
filepath = '/Users/libby/Desktop/506/data_json_files'
directory = os.fsencode(filepath)
cleaned_files = {}
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    with open(filepath +'/'+ filename, 'r') as f:
        if filename.endswith(".json"):
            datastore = f.read()
    articles = datastore.split('{"_id"')
    print(file, len(articles))
    cleaned_files[filename] = []
    for article in articles:
        index = article.find('"story":')
        article = article[index+8:-3].replace('.','').replace('!','').replace('?','').replace(',','').replace('"','').lower()
        cleaned_files[filename].append(article)
neg_sentiments = {}
pos_sentiments = {}
for key in cleaned_files:
    print()
    print(key)
    negative_sentiment = {'perpetrator':0, "violent": 0, "arrest": 0, "gang":0,
    "low-income":0, "urban":0, "un-employed":0, "thug":0, "crime":0, "brute":0, "scam":0, "rob":0, "suspect":0, "dangerous":0,
    "murder":0, "shot": 0, "gun":0, "violence":0, "robbery": 0, "mug":0, "weapon":0, "killed":0, "drug":0, "overdose": 0, "rape":0}
    positive_sentiment = {'worker':0, "working": 0, "parent": 0, "parenting":0,
    "fund-raising":0, "charity":0, "victim":0, "entertainer":0, "actor":0, "actress":0, "hero":0, "heroic":0, "heroes":0, "theater":0, 
    "museum":0, "education" :0, "school":0, "dance":0, "celebration":0, "sport":0}
    for article in cleaned_files[key]:
        article = article.split(" ")
        for word in article:
            if word in negative_sentiment:
                negative_sentiment[word]+=1
            if word in positive_sentiment:
                positive_sentiment[word]+=1
    print(negative_sentiment)
    print(positive_sentiment)