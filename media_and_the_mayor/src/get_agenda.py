import os
import json
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF



# define the required paths
DATASETS = './Datasets/'
RAW_DATASETS = DATASETS + 'Raw/'
PREPROCESSED_DATASETS = DATASETS + 'Preprocessed/'

# number of topics to detect
N_TOPICS = 15
# number of words to use for the representation of each topic
N_TOP_WORDS = 15



def get_agenda_topics(model, feature_names, n_top_words):
	agenda_topics = {}
	for i, topic in enumerate(model.components_):
		agenda_topics[i] = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
		
	return agenda_topics


def create_tf_idf(corpus):
	'''
		Vectorize the vocabulary using tf-idf

		corpus: a list containing all the articles
	'''
	tf_idf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2)
	tf_idf = tf_idf_vectorizer.fit_transform(corpus)
	tf_idf_features = tf_idf_vectorizer.get_feature_names()

	return tf_idf, tf_idf_features



df = pd.read_csv(PREPROCESSED_DATASETS + 'press_releases.csv')
df_temp = pd.read_csv(RAW_DATASETS + 'press_releases.csv')

# drop all the articles published by the mayor's office
# they dominate the dataset and they are mostly just noise
articles = df.loc[df_temp['published_by'] != "Mayor's Office"]['text'].to_list()


tf_idf, tf_idf_features = create_tf_idf(articles)

nmf = NMF(n_components=N_TOPICS, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tf_idf)
agenda_topics = get_agenda_topics(nmf, tf_idf_features, N_TOP_WORDS)


# save agenda for future use
with open(DATASETS + 'agenda.json', 'w') as f:
	f.write(json.dumps(agenda_topics))


datasets = os.listdir(PREPROCESSED_DATASETS)

for file in datasets:
	if file.endswith('.csv'):
		print(file)
		df = pd.read_csv(PREPROCESSED_DATASETS + file)

		for i, article in df.iterrows():
			article = df.iloc[i]['text'].split()

			max_count = 0
			best_topic = None

			for topic in agenda_topics:
				cur_count = 0

				for word in agenda_topics[topic]:
					cur_count += article.count(word)

				if cur_count > max_count:
					best_topic = topic
					max_count = cur_count


			df.at[i, 'agenda topic'] = best_topic

		df.to_csv(PREPROCESSED_DATASETS + file, index=False)















