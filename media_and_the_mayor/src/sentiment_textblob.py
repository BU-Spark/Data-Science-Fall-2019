import textblob
import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def read_data(data):
    doc = data.body.to_numpy()
    doc_summary = data.summary.to_numpy()
    doc_title = data.title.to_numpy()
    return doc, doc_summary, doc_title

def senti_textblob(doc):
    senti = []
    pos, neu, neg = 0, 0, 0
    for d in doc:
        blob = textblob.TextBlob(d, analyzer=textblob.en.sentiments.NaiveBayesAnalyzer())
        if blob.polarity > 0.15:
            senti.append(1)
            pos += 1
        elif blob.polarity < 0.15 and blob.polarity > 0:
            senti.append(0)
            neu += 1
        else:
            senti.append(-1)
            neg += 1
    return senti, pos, neu, neg

def senti_vader(doc):
    vad = SentimentIntensityAnalyzer()
    senti = []
    for d in doc:
        score = vad.polarity_scores(d)
        senti.append([score['neg'], score['neu'], score['pos']])
    return senti

def read_twitter(data):
    doc = data.text.to_numpy()
    return doc

data = pd.read_csv('./mainstream_mayor/wgbh.csv', index_col=False, header=0, names=['ID','author','body','category','date','journal','media','page_number','source','summary','tags','title','url']).fillna('')
doc, summ, title = read_data(data)
senti_value, pos, neu, neg = senti_textblob(doc)
# senti_value = senti_vader(doc)
pd.DataFrame(senti_value).to_csv('./mainstream_senti/wgbh_sentiment.csv')
print(pos, neu, neg)

# keywords=["school", "housing", "youth", "resident", "arts", "library", "service", "community", "street", "program"]
# for j in range(len(keywords)):
#     data = pd.read_csv('./twitter_mayor/'+keywords[j]+'.csv', index_col=False, header=0, names=['tweet_id','Timestamp','likes','retweets','replies','hashtag','text']).fillna('')
#     # doc, summ, title = read_data(data)
#     doc = read_twitter(data)
#     senti_value, pos, neu, neg = senti_textblob(doc)
#     pd.DataFrame(senti_value).to_csv('./twitter_senti/'+keywords[j]+'_senti.csv')
#     print(pos, neu, neg)
    