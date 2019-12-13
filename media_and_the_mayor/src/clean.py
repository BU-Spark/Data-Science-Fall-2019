import os
import pandas as pd
import numpy as np



# define the required paths
DATASETS = './Datasets/'
RAW_DATASETS = DATASETS + 'Raw/'



def convert_to_unix_dates(df):
	'''
		Convert any date to unix timestamp
	'''
	df['date'] = pd.to_datetime(df['date'].str.replace('Updated ', ''), infer_datetime_format=True).astype(np.int64) // 10**9 + 18000

	return df


def remove_empty_articles(df):
	'''
		Remove articles with no body
	'''
	try:
		return df[df['body'].notnull()]
	except:
		return df[df['body_text'].notnull()]



for file in os.listdir(RAW_DATASETS):
    if file.endswith('.csv'):
    	print('Cleaning: ', file)

    	df = pd.read_csv(RAW_DATASETS + file)
    	df = remove_empty_articles(df)
    	df = convert_to_unix_dates(df)

    	df.to_csv(RAW_DATASETS + file)
