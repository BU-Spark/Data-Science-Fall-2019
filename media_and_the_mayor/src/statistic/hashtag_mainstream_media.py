#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 14:32:24 2019

@author: lupeiqing
"""
import pandas as pd
import operator
data_bg=pd.read_csv("boston_globe.csv")
data_bh=pd.read_csv("boston_herald.csv")
print(data_bg.head)
print(data_bh.head)
print(data_bg.dtypes)
operator
map_word={}
for i in data_bg['tags']:
    l=str(i).split(',')
    for j in l:
        if j in map_word:
            map_word[j]+=1
        else:
            map_word[j]=1
for i in data_bh['tags']:
    l=str(i).split(',')
    for j in l:
        if j in map_word:
            map_word[j]+=1
        else:
            map_word[j]=1
delete = [key for key in map_word if map_word[key]<10] 
for i in delete:
    del map_word[i]
sorted_list = sorted(map_word.items(), key=operator.itemgetter(1))
print(sorted_list)
file=open("hashtag_result.txt",'w')
file.write(str(sorted_list))