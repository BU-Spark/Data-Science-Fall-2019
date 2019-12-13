import pandas as pd
import re

keywords_black_nei = []
with open('keywords_neighborhood_black.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        keywords_black_nei.append(line)

keywords_all_nei = []
with open('keywords_neighborhood_all.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        keywords_all_nei.append(line)


def print_coverage(source_path):
    data = pd.read_json(source_path)

    count_black_nei = 0
    count_all_nei = 0

    for i in range(0, len(data['text'])):
        article = data['text'][i]
        relevant = False
        relevant_all = False
        for para in article:
            for str in para:
                for keyword in keywords_black_nei:
                    temp = bool(re.search(keyword, str, re.IGNORECASE))
                    if temp:
                        relevant = True
                        relevant_all = True
                        break
                for keyword in keywords_all_nei:
                    temp = bool(re.search(keyword, str, re.IGNORECASE))
                    if temp:
                        relevant_all = True
                        break
            if relevant:
                break
        if relevant:
            count_black_nei += 1
        if relevant_all:
            count_all_nei += 1
    print(count_black_nei, count_all_nei, len(data['text']))


if __name__ == '__main__':
    print(keywords_black_nei)
    print(len(keywords_black_nei))
    print(keywords_all_nei)
    print(len(keywords_all_nei))
    print_coverage('classified data/bostonglobe2014.json')
    print_coverage('classified data/bostonglobe2015.json')
    print_coverage('classified data/bostonglobe2016.json')
    print_coverage('classified data/bostonglobe2017.json')
    print_coverage('classified data/bostonglobe2018.json')
    print_coverage('classified data/wbur_2014.json')
    print_coverage('classified data/wbur_2015.json')
    print_coverage('classified data/wbur_2016.json')
    print_coverage('classified data/wbur_2017.json')
    print_coverage('classified data/wbur_2018.json')
    print_coverage('classified data/wgbh.json')
