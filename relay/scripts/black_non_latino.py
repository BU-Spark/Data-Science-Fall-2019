#keeping only black owner businesses from preprocessed dataset collected from SBA

import numpy as np
import pandas as pd

from pandas import *


#reading cleaned dataset
df = pd.read_csv('../datasets/small_disadvantaged_proc_owners_full_no_duplicates_fin_names.csv', index_col=0)

#keeping only black owned-led businesses
df_new = df[df['race_ethnicity_alt']=='B_NL']

#save to csv
df_new.to_csv('../datasets/small_disadvantaged_bl_alt.csv')
