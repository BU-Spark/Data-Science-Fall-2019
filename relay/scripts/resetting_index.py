#simple script to reset csv dataset index
import numpy as np
import pandas as pd

from pandas import *


#reading dataset
df = pd.read_csv('../datasets/black_non_latino/data_all_bl.csv', index_col=0)

df = df.reset_index(drop=True)


#save to csv
df.to_csv('../datasets/black_non_latino/data_all_bl.csv')
