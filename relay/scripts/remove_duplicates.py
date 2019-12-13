#duplicates removal from original dataset
#removing nan entries
#removing entries with same phone numbers


from more_itertools import unique_everseen
import pandas as pd
from pandas import *

#reading dataset
df = pd.read_csv('../datasets/finals/all_data_ref_Name_no_dup.csv', index_col=0)
print (df.columns)

print(df.shape)

#data manipulation
df = df.replace('Not Available',np.NaN)
df = df.replace('NA',np.NaN)
dupes = df.duplicated(subset=['USBC_phone'])
dupes[df['USBC_phone'].isnull()] = False
df_dup = df[dupes]
df = df[~dupes]


# Write the results to a different file
df.to_csv('../datasets/finals/all_data_ref_usbc_no_dup.csv')
df_dup.to_csv('../datasets/finals/all_data_ref_usbc_only_dup.csv')
print (df.shape, df_dup.shape)


