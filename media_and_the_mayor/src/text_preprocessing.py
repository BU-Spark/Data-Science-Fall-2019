import os
import re
from string import punctuation

import numpy as np
import pandas as pd

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer



# define the required paths
DATASETS = './Datasets/'
RAW_DATASETS = DATASETS + 'Raw/'
PREPROCESSED_DATASETS = DATASETS + 'Preprocessed/'



stopwords_list = stopwords.words('english')


# load the dataset
for dataset in os.listdir(RAW_DATASETS):
	if dataset.endswith('.csv'):
		df = pd.read_csv(RAW_DATASETS + dataset)
		# drop leftover indices
		for column in df.columns:
			if column.startswith('Unnamed: '):
				df = df.drop(columns=column)

		# merge title, tags, summary, body
		# this helps give some extra way to more important words
		df['text'] = df['title'].map(str) + df['tags'].map(str) + df['summary'].map(str) + df['body'].map(str)
		df = df.drop(columns=['title', 'tags', 'summary', 'body'])

		# standard text pre-processing
		df['text'] = df['text'].str.lower()
		df['text'] = df['text'].apply(word_tokenize)
		df['text'] = [[word for word in article if word not in stopwords_list and word not in punctuation] for article in df['text']]
		df['text'] = [' '.join([WordNetLemmatizer().lemmatize(word) for word in article]) for article in df['text']]


		if not os.path.exists(PREPROCESSED_DATASETS):
			os.mkdir(PREPROCESSED_DATASETS)

		df.to_csv(PREPROCESSED_DATASETS + dataset, index=False)
		print('Saved: ', dataset)



