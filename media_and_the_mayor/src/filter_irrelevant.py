import os

import numpy as np
import pandas as pd

from keras.models import load_model



# define the required paths
DATASETS = './Datasets/'
VECTORIZED_DATASETS = DATASETS + 'Doc2Vec/'
FILTERED_DATASETS = DATASETS + 'Filtered/'

MODELS = './Models/'



datasets = os.listdir(VECTORIZED_DATASETS)
model = load_model(MODELS + 'relevance_classifier.h5')


if not os.path.exists(FILTERED_DATASETS):
	os.mkdir(FILTERED_DATASETS)

for file in datasets:
	if file.endswith('.csv'):
		df = pd.read_csv(VECTORIZED_DATASETS + file)

		X = []
		for article_vector in df['text']:
			X.append(' '.join(article_vector.strip('[').strip(']').split()).split(' '))

		X = np.array(X)
		# predict the article's relevance
		relevance = model.predict_classes(X)

		# keep only the relevant
		df = df.loc[np.where(relevance==1)]

		df.to_csv(FILTERED_DATASETS + file, index=False)

