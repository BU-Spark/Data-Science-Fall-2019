import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn


def print_top_words(model, feature_names, n_top_words, file_name):
    f = open(file_name, 'w+')
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx, file=f)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]), file=f)
    f.close()
    print()


def get_topics(file, file2):
    df = pd.read_csv(file)
    print('Processing ',file.replace('..//relevant data//', ''),". It may take a long time.")
    stop_words = ['said', 'says', 'boston', 'globe', 'men', 'women', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                  'Friday', 'Saturday', 'Sunday', 'Boston', 'people', 'dorchester', 'walsh', 'Dorchester', 'Roxbury',
                  'Walsh', 'Mattapan', 'Dudley', 'Park', 'new', 'city', 'City', 'time', 'Square', 'district', 'year',
                  'years']
    for i in range(len(df['text'])):
        for word in stop_words:
            df['text'][i] = df['text'][i].replace(word, ' ')

    tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    max_features=10000,
                                    stop_words='english',
                                    max_df=0.5,
                                    min_df=10)
    tf = tf_vectorizer.fit_transform(df['text'])

    # cluster number
    lda = LatentDirichletAllocation(n_components=5, max_iter=50,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    lda.fit(tf)

    # topic number
    n_top_words = 5
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words, file2)
    data = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
    pyLDAvis.show(data)

    return


if __name__ == '__main__':
    get_topics('classified data//bostonglobe2014.csv', '5topics_all.txt')
    # get_topics('classified data//bostonglobe2015.csv', '5topics_all.txt')
    # get_topics('classified data//bostonglobe2016.csv', '5topics_all.txt')
    # get_topics('classified data//bostonglobe2017.csv', '5topics_all.txt')
    # get_topics('classified data//bostonglobe2018.csv', '5topics_all.txt')

    get_topics('relevant data//bostonglobe2014.csv', '5topics_black.txt')
    # get_topics('relevant data//bostonglobe2015.csv', '5topics_black.txt')
    # get_topics('relevant data//bostonglobe2016.csv', '5topics_black.txt')
    # get_topics('relevant data//bostonglobe2017.csv', '5topics_black.txt')
    # get_topics('relevant data//bostonglobe2018.csv', '5topics_black.txt')
