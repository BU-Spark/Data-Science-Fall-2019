import pandas as pd
from collections import Counter
import string
from nltk.corpus import stopwords
import csv

test = pd.read_csv('relevant data/bostonglobe2018.csv')


def getMostCommonWords(reviews, n_most_common, stopwords=None, output=False):
    flattened_reviews = [word for review in reviews for word in \
                         review.lower().split()]
    flattened_reviews = [''.join(char for char in review if \
                                 char not in string.punctuation) for \
                         review in flattened_reviews]
    if stopwords:
        flattened_reviews = [word for word in flattened_reviews if \
                             word not in stopwords]

    flattened_reviews = [review for review in flattened_reviews if review]
    mycounter = Counter(flattened_reviews).most_common(n_most_common)
    if output:
        with open("wgbh_output.csv", "a", newline='', encoding='utf-8') as fp:
            wr = csv.writer(fp, dialect='excel')
            for item in mycounter:
                wr.writerow(item, )
    return mycounter


print(getMostCommonWords(test['text'], 500, stopwords.words('english'), True))
