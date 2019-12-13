import pandas as pd
import re

keywords = []
with open('keywords_neighborhood_black.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        keywords.append(line)

with open('keywords_more.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        keywords.append(line)


def keywords_filter(source_path, target_path):
    data = pd.read_json(source_path)

    count = 0
    all_articles = {'text': []}

    for i in range(0, len(data['text'])):
        article = data['text'][i]
        relevant = False
        for para in article:
            for str in para:
                for keyword in keywords:
                    temp = bool(re.search(keyword, str, re.IGNORECASE))
                    if temp:
                        relevant = True
                        break
            if relevant:
                break
        if relevant:
            count = count + 1
            s = ''
            for para in article:
                for str in para:
                    s = s + str
            all_articles['text'].append([s])
    df = pd.DataFrame(all_articles, columns=['text'])
    df.to_csv(target_path, encoding='utf-8_sig', index=False)
    print(count)


if __name__ == '__main__':
    print(keywords)
    print(len(keywords))
    keywords_filter('classified data/bostonglobe2014.json', 'relevant data/bostonglobe2014.csv')
    keywords_filter('classified data/bostonglobe2015.json', 'relevant data/bostonglobe2015.csv')
    keywords_filter('classified data/bostonglobe2016.json', 'relevant data/bostonglobe2016.csv')
    keywords_filter('classified data/bostonglobe2017.json', 'relevant data/bostonglobe2017.csv')
    keywords_filter('classified data/bostonglobe2018.json', 'relevant data/bostonglobe2018.csv')
    keywords_filter('classified data/wbur_2014.json', 'relevant data/wbur_2014.csv')
    keywords_filter('classified data/wbur_2015.json', 'relevant data/wbur_2015.csv')
    keywords_filter('classified data/wbur_2016.json', 'relevant data/wbur_2016.csv')
    keywords_filter('classified data/wbur_2017.json', 'relevant data/wbur_2017.csv')
    keywords_filter('classified data/wbur_2018.json', 'relevant data/wbur_2018.csv')
    keywords_filter('classified data/wgbh.json', 'relevant data/wgbh.csv')

    # keywords = ['']
    # keywords_filter('classified data/bostonglobe2014.json', 'classified data/bostonglobe2014.csv')
    # keywords_filter('classified data/bostonglobe2015.json', 'classified data/bostonglobe2015.csv')
    # keywords_filter('classified data/bostonglobe2016.json', 'classified data/bostonglobe2016.csv')
    # keywords_filter('classified data/bostonglobe2017.json', 'classified data/bostonglobe2017.csv')
    # keywords_filter('classified data/bostonglobe2018.json', 'classified data/bostonglobe2018.csv')
    # keywords_filter('classified data/wbur_2014.json', 'classified data/wbur_2014.csv')
    # keywords_filter('classified data/wbur_2015.json', 'classified data/wbur_2015.csv')
    # keywords_filter('classified data/wbur_2016.json', 'classified data/wbur_2016.csv')
    # keywords_filter('classified data/wbur_2017.json', 'classified data/wbur_2017.csv')
    # keywords_filter('classified data/wbur_2018.json', 'classified data/wbur_2018.csv')
    # keywords_filter('classified data/wgbh.json', 'classified data/wgbh.csv')
