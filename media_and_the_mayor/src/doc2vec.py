import os
import pandas as pd

from gensim.models.doc2vec import Doc2Vec, TaggedDocument



# train mode for doc2vec
TRAIN = False

# define the required paths
MODELS = './Models/'
DATASETS = './Datasets/'
PREPROCESSED_DATASETS = DATASETS + 'Preprocessed/'
DOC2VEC_DATASETS = DATASETS + 'Doc2Vec/'

# define the training set
TRAINING_FILES = ['press_releases.csv', 'boston_herald.csv']

# doc2vec hyperparamers
EPOCHS = 100
EMBEDDING_SIZE = 200
ALPHA = 0.025



def get_training_set():
    '''
        Fetch and concatenate all the datasets 
        defined in TRAINING_FILES to create the training dataset
    '''
    dataframes = []

    for file in TRAINING_FILES:
        dataframes.append(pd.read_csv(PREPROCESSED_DATASETS + file))

    df = dataframes[0]
    for i in range(1, len(dataframes), 1):
        df.append(dataframes[i])

    return df


def train(training_articles):
    '''
        Train the doc2vec model

        training_articles: a list containing all the datasets to be included in the training set
    '''
    documents = [TaggedDocument(article.split(' '), [i]) for i, article in enumerate(training_articles)]

    model = Doc2Vec(
        size = EMBEDDING_SIZE,
        alpha = ALPHA, 
        min_alpha = 0.00025,
        min_count = 1,
        dm = 1
    )
      
    model.build_vocab(documents)

    for epoch in range(EPOCHS):
        print('Epoch: ', epoch)

        model.train(documents, total_examples=model.corpus_count, epochs=model.iter)
        
        model.alpha -= 0.0002
        model.min_alpha = model.alpha

    return model


def save(model):
    '''
        Save the model for future use
    '''
    if not os.path.exists(MODELS):
        os.mkdir(MODELS)

    model.save(MODELS + 'd2v.model')


def fit(model, articles):
    '''
        Fit unseen data to the trained model

        model: the pre-trained model
        articles: a list of the articles to fit
    '''
    vectors = []
    
    articles = [article.split(' ') for article in articles]
    for article in articles:
        vectors.append(model.infer_vector(article))

    return pd.Series(vectors)


def save_vectorized_dataset(df, file_name):
    '''
        Save the dataframe to a new file
    '''
    if not os.path.exists(DOC2VEC_DATASETS):
        os.mkdir(DOC2VEC_DATASETS)
    
    df.to_csv(DOC2VEC_DATASETS + file_name, index=False)



if TRAIN:
    df_training = get_training_set()

    model = train(df_training['text'])
    save(model)

model = Doc2Vec.load(MODELS + 'd2v.model')

datasets = os.listdir(PREPROCESSED_DATASETS)
for file in datasets:
    if file.endswith('.csv'):
        print('Processing: ', file)
        
        df = pd.read_csv(PREPROCESSED_DATASETS + file)

        df['text'] = fit(model, df['text'])
        save_vectorized_dataset(df, file)




