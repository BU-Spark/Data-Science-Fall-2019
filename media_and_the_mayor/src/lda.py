import csv
import numpy as np
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

def import_data(filename):
    X = []
    with open(filename, 'r') as f:
        csv_reader = csv.reader(f)
        header = next(csv_reader)
        for line in csv_reader:
            X.append(line[4])
        
    return X

def print_top_words(model, feature_names, n_top_words):
    messages = []
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
        messages.append(message)
    return messages    

X = import_data("news_item.csv")
output = []

tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                   max_features=30,
                                   stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(X)

tf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=30, stop_words='english')
tf = tf_vectorizer.fit_transform(X)

nmf = NMF(n_components=10, random_state=1,
          beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,
          l1_ratio=.5).fit(tfidf)
print("Topics of NMF:")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
output.append(print_top_words(nmf, tfidf_feature_names, 30))

lda = LatentDirichletAllocation(n_components = 10, learning_method='online', max_iter=5, random_state=0)
lda.fit(tf)

print("Topics of LDA:")
tf_feature_names = tf_vectorizer.get_feature_names()
output.append(print_top_words(lda, tf_feature_names, 30))

outfile = open("Topic Words.csv", 'w')
csv_writer = csv.writer(outfile, dialect='excel')
for elem in output:
    csv_writer.writerow(elem)
