#SBA data manipulation and simple column names and entries processing
#dropping nan values

import numpy as np
import pandas as pd

from pandas import *

import urllib
from urllib.request import pathname2url
#from urlparse import urlparse

#reading dataset
df = pd.read_csv('../datasets/small_disadvantaged.csv', index_col=0)


#changin column names
df.rename(columns={'unknown':'Contact'}, inplace=True)
df.rename(columns={'unknown.1':'Position'}, inplace=True)
df.rename(columns={'Address, line 1':'Address_line_1'}, inplace=True)
df.rename(columns={'Address, line 2':'Address_line_2'}, inplace=True)
df.rename(columns={'Capabilities Narrative':'Capabilities_narrative'}, inplace=True)
df.rename(columns={'Name of Firm':'Name_of_firm'}, inplace=True)
df.rename(columns={'Trade Name':'Trade_name'}, inplace=True)

#dropping nan values
df.dropna(subset=['Contact'],axis='rows',inplace=True)


#percent encoding Contact names to be used in naming algorithm
names_array = df['Contact'].values
urls_list=[]
for name in names_array:
	urls_list.append(pathname2url(name))


df['perc_encoding']=urls_list

#save to csv
df.to_csv('../datasets/small_disadvantaged_proc.csv')
