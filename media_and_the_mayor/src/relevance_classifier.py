import numpy as np
import pandas as pd

from keras.models import Sequential
from keras.layers import Dense



# define the required paths
MODELS = './Models/'
VECTORIZED_DATASETS = './Datasets/Doc2Vec/'

# neural network hyperparamets
EPOCHS = 23
BATCH_SIZE = 256

# irrelevant Boston Herald categories
IRRELEVANT_CATEGORIES = [
	'lifestyle,travel', 
	'entertainment,arts-culture', 
	'lifestyle,food-beverage', 
	'entertainment,movies', 
	'entertainment,horoscope', 
	'entertainment,celebrity-news', 
	'entertainment,television', 
	'obituaries', 
	'lifestyle', 
	'entertainment', 
	'lifestyle,style-fashion', 
	'entertainment,music', 
	'tag,2020-election', 
	'tag,state-house', 
	'tag,donald-trump', 
	'sports,celtics', 
	'sports,college-sports', 
	'sports,red-sox', 
	'sports,high-school-sports', 
	'sports,patriots', 
	'sports,bruins', 
	'news,national-news', 
	'news,world-news', 
]

# relevant Boston Herald categories
RELEVANT_CATEGORIES = [
	'news,local-news',   
	'tag,boston-city-hall', 
	'tag,your-tax-dollars-at-work',
]

# neutral Boston Herald categories
NEUTRAL_CATEGORIES = [
	'opinion,letters', 
	'opinion,editorials', 
	'news,columnists', 
	'news,health', 
	'news,business', 
	'news,politics', 
	'opinion,op-ed', 
	'news,crime-public-safety', 
	'news,massachusetts-news' 
]



def build_model():
	'''
		Implementation of a 5 layer Feed Forward Neural Network
	'''
	model = Sequential()
	model.add(Dense(200, input_dim=200, activation='relu'))
	model.add(Dense(200, activation='relu'))
	model.add(Dense(200, activation='relu'))
	model.add(Dense(200, activation='relu'))
	model.add(Dense(200, activation='relu'))
	model.add(Dense(2, activation='softmax'))

	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

	return model



df = pd.read_csv(VECTORIZED_DATASETS + 'boston_herald.csv')

# sample the irrelevant articles in order to even out a bit the training set
irrelevant_articles = df.loc[df['category'].isin(IRRELEVANT_CATEGORIES)].sample(frac=0.5)
relevant_articles = df.loc[df['category'].isin(RELEVANT_CATEGORIES)]
neutral_articles = df.loc[df['category'].isin(NEUTRAL_CATEGORIES)]


relevant_articles = relevant_articles.append(pd.read_csv(VECTORIZED_DATASETS + 'press_releases.csv'), sort=False)


irrelevant_articles = pd.DataFrame(irrelevant_articles['text'])
relevant_articles = pd.DataFrame(relevant_articles['text'])


irrelevant_articles['class'] = 0
relevant_articles['class'] = 1


df_training = irrelevant_articles.append(relevant_articles)


X_train = []
for article_vector in df_training['text']:
	X_train.append(' '.join(article_vector.strip('[').strip(']').split()).split(' '))


X_train = np.array(X_train)
# one-hot encode the target classes
y_train = pd.get_dummies(df_training['class'])


model = build_model()
model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE)
loss, accuracy = model.evaluate(X_train, y_train)

print('Test set - loss: {} - accuracy: {}'.format(loss, accuracy))

# save the classifier for future use
model.save(MODELS + 'relevance_classifier.h5')




