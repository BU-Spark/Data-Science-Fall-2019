#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
we count how many news items that contains those topics by simply string matching in news body text.
"""

import pandas as pd
import operator
data_bg=pd.read_csv("boston_globe.csv")
data_bh=pd.read_csv("boston_herald.csv")
data_wbur=pd.read_csv("wbur.csv")
data_wgbh=pd.read_csv("wgbh.csv")
f = open("List.txt", "r")
word_list=f.readlines()
word_list=[i.replace("\n","") for i in word_list]
map_word={}
for i in word_list:
    sum=0;
    for j in data_bg["body"]:
        if i in j:
            sum+=1
    for j in data_bh["body"]:
        if i in j:
            sum+=1
    for j in data_wbur["body"]:
        if i in j:
            sum+=1
    for j in data_wgbh["body"]:
        if i in j:
            sum+=1
    map_word[i]=sum
sorted_list = sorted(map_word.items(), key=operator.itemgetter(1))
print(sorted_list)
    