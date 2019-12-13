import nltk
import numpy as np
import pandas as pd
from string import digits
import re
import logging
import gensim
from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import PCA
from gensim.models import Word2Vec
from gensim.models import Doc2Vec

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

def read_data(data):
    doc = data.body.to_numpy()
    doc_summary = data.summary.to_numpy()
    doc_title = data.title.to_numpy()
    return doc, doc_summary, doc_title

def read_twitter(data):
    doc = data.text.to_numpy()
    return doc

def split_sentence(doc):
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sents = sent_tokenizer.tokenize(doc)
    return sents

def clean_sentence(words):
    for i in range(len(words)):
        words[i] = re.sub(r'\b\d+(?:\.\d+)?\s+', '', words[i])
    return words

def to_lower(words):
    # to lower case
    return words.lower()

def eli_stopword(words):
    # stopwords
    stop_words = stopwords.words('english')
    for w in ['!',',','.','?','-s','-ly','</s>','s']:
        stop_words.append(w)
    words = [word for word in words if word not in stop_words]
    return words

def tokenize(sentence):
    # tokenizer
    words = WordPunctTokenizer().tokenize(sentence)
    return words

def stemming(words):
    # stemming
    stemmer = SnowballStemmer('english')
    word_stem = []
    for word in words:
        word_stem.append(stemmer.stem(word))
    return word_stem

def frequency_list(words):
    # frequency
    freq_dist = nltk.FreqDist(words)
    freq_list = []
    for i in range(len(freq_dist.values())):
        freq_list.append([list(freq_dist.keys())[i], list(freq_dist.values())[i]])
    return freq_list

def tf_idf(sentences):
    # Bag of words model
    vect = CountVectorizer(analyzer='word', max_df=0.75, min_df=0.25)
    vect.fit(sentences)
    X = vect.transform(sentences)
    wordlist = pd.DataFrame(vect.get_feature_names())
    wordlist.to_csv('./wordlist/boston_globe_50%wordlist.csv')
    # Calculate tf-idf feature
    trans = TfidfTransformer()
    trans.fit(X)
    tfidf = trans.transform(X)
    return tfidf.toarray()

def doc2vec(words):
    doc = []
    count = 0
    for w in words:
        # print(w)
        doc.append(gensim.models.doc2vec.TaggedDocument(w, [str(count)]))
        count+=1
    # model = Doc2Vec(doc, min_count=1, iter=20, workers=5)
    # model.save("word2vec.model")
    model = Doc2Vec.load("doc2vec.bin")
    sents = []
    vec = []
    for w in words:
        sents.append(tokenize(w))
    for s in sents:
        vec.append(model.infer_vector(s))
    return vec

def PCA_model(data):
    pca = PCA(n_components=2)
    pca.fit(data)
    X = pca.transform(data)
    return X

def normalize(doc):
    sentences = clean_sentence(split_sentence(doc))
    words = []
    for i in range(len(sentences)):
        words = eli_stopword(tokenize(to_lower(sentences[i])))
    # d = []
    stem_words = stemming(words)
    d = ' '.join(stem_words)
    return d
# freq_list = frequency_list(words)

# doc = "Life  is  not  easy for  any  of  us. We  must  work,and  above  all \
# we must  believe  in  ourselves. We  must  believe  that  each  one  of  us  is  \
# able to  do  something well, and  that, when  we  discover  what 0 this  something  is,\
# we  must  work  hard  at  it  until we succeed."

# keywords=["school", "housing", "youth", "resident", "arts", "library", "service", "community", "street", "program"]
# for j in range(len(keywords)):
#     data = pd.read_csv('./twitter_lemmatization_cleaned/'+keywords[j]+'.csv', index_col=False, header=0, names=['tweet_id','Timestamp','likes','retweets','replies','hashtag','text']).fillna('')
#     # doc, summ, title = read_data(data)
#     doc = read_twitter(data)
#     for i in range(len(doc)):
#         doc[i] = normalize(doc[i])
#     data.text = doc
#     data.to_csv('./twitter_process/'+keywords[j]+'.csv')

#     data = pd.read_csv('./twitter_process/'+keywords[j]+'.csv', index_col=False, header=0, names=['tweet_id','Timestamp','likes','retweets','replies','hashtag','text']).fillna('')
#     doc = read_twitter(data)
#     d = []
#     for i in range(len(doc)):
#         d.append(normalize(doc[i]))
#     doc2vec_matrix = doc2vec(doc)
#     doc2vec_pca = pd.DataFrame(PCA_model(doc2vec_matrix))
#     doc2vec_pca.to_csv('./twitter_doc2vec/'+keywords[j]+'.csv')

# data = pd.read_csv('./mainstream_mayor/boston_herald.csv', index_col=False, header=0, names=['ID','author','body','category','date','journal','media','page_number','source','summary','tags','title','url']).fillna('')
# doc, summ, title = read_data(data)
# data_set = [doc, summ, title]
# for j in range(len(data_set)):
#     d = []
#     for i in range(len(data_set[j])):
#         d.append(normalize(data_set[j][i]))
#     data_set[j] = d
# data.body = data_set[0]
# data.summary = data_set[1]
# data.title = data_set[2]
# data.to_csv('./mainstream_process/boston_herald_process.csv')

# data = pd.read_csv('./mainstream_process/boston_herald_process.csv', index_col=False, header=0, names=['0','ID','author','body','category','date','journal','media','page_number','source','summary','tags','title','url']).fillna('')
# doc, _, _ = read_data(data)
# d = []
# for i in range(len(doc)):
#     d.append(normalize(doc[i]))
# doc2vec_matrix = doc2vec(doc)
# doc2vec_pca = pd.DataFrame(PCA_model(doc2vec_matrix))
# doc2vec_pca.to_csv('./mainstream_doc2vec/boston_herald_doc2vec.csv')
# doc2vec_matrix.to_csv('./mainstream_doc2vec/wgbh_doc2vec.csv')
# tfidf_matrix = pd.DataFrame(tf_idf(doc))
# tfidf_matrix.to_csv('boston_globe_word2vec.csv')


