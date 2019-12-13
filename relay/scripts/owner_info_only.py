#only keeping entries from dataset with owner/contact info - discarding entries with no such information
import numpy as np
import pandas as pd

from pandas import *

import urllib
from urllib.request import pathname2url
#from urlparse import urlparse

#reading dataset
df = pd.read_csv('../datasets/data_all_no_naics_proc_no_duplicates.csv', index_col=0)


#dropping nan values
df.dropna(subset=['Position'],axis='rows',inplace=True)



#save to csv
df.to_csv('../datasets/data_all_no_naics_proc_no_duplicates_owners_full.csv')
