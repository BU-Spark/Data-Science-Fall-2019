import pandas as pd


def combine(files, output):
    all_articles = {}
    all_articles['text'] = []

    for file in files:
        df = pd.read_json(file)
        for article in df['text']:
            all_articles['text'].append(article)
    df = pd.DataFrame(all_articles, columns=['text'])
    df.to_json(output)


if __name__ == '__main__':
    bostonglobe2014 = ['raw data//bostonglobe2014_1.json', 'raw data//bostonglobe2014_2.json']
    bostonglobe2015 = ['raw data//bostonglobe2015_1.json']
    bostonglobe2016 = ['raw data//bostonglobe2016_1.json', 'raw data//bostonglobe2016_2.json']
    bostonglobe2017 = ['raw data//bostonglobe2017_1.json']
    bostonglobe2018 = ['raw data//bostonglobe2018_1.json', 'raw data//bostonglobe2018_2.json', 'raw data//bostonglobe2018_3.json']
    combine(bostonglobe2014, '..//classified data//bostonglobe2014.json')
    combine(bostonglobe2015, '..//classified data//bostonglobe2015.json')
    combine(bostonglobe2016, '..//classified data//bostonglobe2016.json')
    combine(bostonglobe2017, '..//classified data//bostonglobe2017.json')
    combine(bostonglobe2018, '..//classified data//bostonglobe2018.json')
