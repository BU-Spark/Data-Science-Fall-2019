#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 22:48:34 2019

@author: lupeiqing
"""

import pandas as pd
arts=pd.read_csv("/Users/lupeiqing/Desktop/cs506/twitter_process/arts.csv")
community=pd.read_csv("/Users/lupeiqing/Desktop/cs506/twitter_process/community.csv")
housing=pd.read_csv("/Users/lupeiqing/Desktop/cs506/twitter_process/housing.csv")
library=pd.read_csv("/Users/lupeiqing/Desktop/cs506/twitter_process/library.csv")
program=pd.read_csv("/Users/lupeiqing/Desktop/cs506/twitter_process/program.csv")
resident=pd.read_csv("/Users/lupeiqing/Desktop/cs506/twitter_process/resident.csv")
school=pd.read_csv("/Users/lupeiqing/Desktop/cs506/twitter_process/school.csv")
services=pd.read_csv("/Users/lupeiqing/Desktop/cs506/twitter_process/services.csv")
street=pd.read_csv("/Users/lupeiqing/Desktop/cs506/twitter_process/street.csv")
youth=pd.read_csv("/Users/lupeiqing/Desktop/cs506/twitter_process/youth.csv")
print(arts.info(),arts['likes'].sum(),arts['retweets'].sum(),arts['replies'].sum())
print(community.info(),community['likes'].sum(),community['retweets'].sum(),community['replies'].sum())
print(housing.info(),housing['likes'].sum(),housing['retweets'].sum(),housing['replies'].sum())
print(library.info(),library['likes'].sum(),library['retweets'].sum(),library['replies'].sum())
print(program.info(),program['likes'].sum(),program['retweets'].sum(),program['replies'].sum())
print(resident.info(),resident['likes'].sum(),resident['retweets'].sum(),resident['replies'].sum())
print(school.info(),school['likes'].sum(),school['retweets'].sum(),school['replies'].sum())
print(services.info(),services['likes'].sum(),services['retweets'].sum(),services['replies'].sum())
print(street.info(),street['likes'].sum(),street['retweets'].sum(),street['replies'].sum())
print(youth.info(),youth['likes'].sum(),youth['retweets'].sum(),youth['replies'].sum())