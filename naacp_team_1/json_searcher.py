import os
import json
filepath = '/home/harrison/Desktop/CS506/NAACP-Media-Research/data_json_files'
directory = os.fsencode(filepath)
cleaned_files = {}
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    with open(filepath +'/'+ filename, 'r') as f:
        if filename.endswith(".json"):
            datastore = f.read()
    articles = datastore.split('{"_id"')
    cleaned_files[filename] = []
    for article in articles:
        index = article.find('"story":')
        article = article[index+8:-3].replace('.','').replace('!','').replace('?','').replace(',','').replace('"','').lower()
        cleaned_files[filename].append(article)
neg_sentiments = {}
pos_sentiments = {}
for key in cleaned_files:
    negative_sentiment = {'perpetrator':0, "violent": 0, "arrest": 0, "gang":0,
    "low-income":0, "urban":0, "un-employed":0, "thug":0, "brute":0, "scam":0, "rob":0, "suspect":0, "dangerous":0}
    positive_sentiment = {'worker':0, "working": 0, "parent": 0, "parenting":0,
    "fund-raising":0, "charity":0, "victim":0, "entertainer":0, "actor":0, "actress":0, "hero":0, "heroic":0, "heroes":0}
    for article in cleaned_files[key]:
        article = article.split(" ")
        for word in article:
            if word in negative_sentiment:
                negative_sentiment[word]+=1
            if word in positive_sentiment:
                positive_sentiment[word]+=1
    neg_sentiments[key] = negative_sentiment
    pos_sentiments[key] = positive_sentiment

negative_count = {}
for area in neg_sentiments:
    sum = 0
    #print(sentiments[area])
    for key in neg_sentiments[area]:
        sum += neg_sentiments[area][key]
    negative_count[area[:-10]] = sum

print("Count of negative words by section of the Boston")
print(negative_count)

positive_count ={}
for area in pos_sentiments:
    sum = 0
    #print(sentiments[area])
    for key in pos_sentiments[area]:
        sum += pos_sentiments[area][key]
    positive_count[area[:-10]] = sum

print("Count of positive words by section of the Boston")
print(positive_count)
