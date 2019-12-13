from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import time

data = [pd.read_csv('classified data/bostonglobe2014.csv'),
        pd.read_csv('classified data/bostonglobe2015.csv'),
        pd.read_csv('classified data/bostonglobe2016.csv'),
        pd.read_csv('classified data/bostonglobe2017.csv'),
        pd.read_csv('classified data/bostonglobe2018.csv'),
        pd.read_csv('classified data/wbur_2014.csv'),
        pd.read_csv('classified data/wbur_2015.csv'),
        pd.read_csv('classified data/wbur_2016.csv'),
        pd.read_csv('classified data/wbur_2017.csv'),
        pd.read_csv('classified data/wbur_2018.csv'),
        pd.read_csv('classified data/wgbh.csv')]

analyzer = SentimentIntensityAnalyzer()

print(len(data))
print(len(data[0]))
print(data[0]['text'][0])
print(analyzer.polarity_scores(data[0]['text'][0]))

result = []
for i in range(len(data)):
    print(i)
    print(time.asctime(time.localtime(time.time())))
    pos = 0
    neu = 0
    neg = 0
    for j in range(len(data[i])):
        text = data[i]['text'][j]
        vs = analyzer.polarity_scores(text)
        if vs['compound'] >= 0.05:
            pos += 1
        elif vs['compound'] <= -0.05:
            neg += 1
        else:
            neu += 1
    print(len(data[i]), pos, neu, neg, pos + neu + neg)
    result.append([pos, neu, neg])

row = ['pos', 'neu', 'neg']
result_df = pd.DataFrame(columns=row, data=result)
result_df.to_csv('sentiment_analysis_all.csv')
