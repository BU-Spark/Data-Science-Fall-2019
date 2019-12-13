#keeping only hispanic entries from SBA cleaned dataset

import numpy as np
import pandas as pd

from pandas import *


#reading dataset
df = pd.read_csv('../datasets/small_disadvantaged_proc_owners_full_no_duplicates_fin_names.csv', index_col=0)

#filtering hispanic entries
df_new = df[df['race_ethnicity_alt']=='HL']

#save to csv
df_new.to_csv('../datasets/small_disadvantaged_hl_alt.csv')
