import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def cleanFiles():
    filepath = 'C:\\Users\\alexl\\Desktop\\NAACP-Media-Research\\data_json_files'

    directory = os.fsencode(filepath)
    cleaned_files = {}
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        with open(filepath + '/' + filename, 'r', encoding='utf-8') as f:
            if filename.endswith(".json"):
                datastore = f.read()
        articles = datastore.split('{"_id"')
        cleaned_files[filename] = []
        for article in articles:
            index = article.find('"story":')
            article = article[index+8:-3].replace('.', '').replace('!', '').replace('?', '').replace(',', '').replace('"', '').lower()
            cleaned_files[filename].append(article)

    result_list = []
    for key in cleaned_files:
        for article in cleaned_files[key]:
            result = {"Id": key, "Text": article}
            result_list.append(result)

    save_df = pd.DataFrame(result_list)
    save_df.to_csv("data_distinctive_words.csv", index=False)

    return cleaned_files


def run_tfidf(files):
    df = pd.read_csv('data_distinctive_words.csv', error_bad_lines=False, low_memory=False)
    df1 = df['Text']
    df1 = df1.dropna()
    idf = TfidfVectorizer(stop_words='english')
    idf.fit_transform(df1)
    feature_names = np.array(idf.get_feature_names())

    # Answer_List = []
    # for key in files:
    #     for article in files[key]:
    #         article = article.split(" ")
    #         response = idf.transform(article)
    #         sorted_nzs = np.argsort(response.data)[:-(10 + 1):-1]
    #         Answer_List.append(feature_names[response.indices[sorted_nzs]])

    Answer_List = []
    currAreaList = []
    for key in files:
        for article in files[key]:
            article = article.split(" ")
            currAreaList.extend(article)

        response = idf.transform(currAreaList)
        sorted_nzs = np.argsort(response.data)[:-(30 + 1):-1]  # top_30 keywords
        Answer_List.append(feature_names[response.indices[sorted_nzs]])
        currAreaList.clear()

    regions = ['allston', 'back_bay', 'beacon_hill', 'brighton', 'charles_town', 'chinatown', 'dorchester',
               'downtown', 'east_boston', 'fenway', 'herald', 'hyde_park', 'jamaica_plain', 'kenmore', 'mattapan',
               'mission_hill', 'north_end', 'roslindale', 'roxbury', 'south_boston', 'south_end', 'west_end',
               'west_roxbury']  # 0-22

    top_distinct_each_region = []
    for i in range(len(Answer_List)):
        print(regions[i])
        print(Answer_List[i])
        print('\n')
        # print('\n'.join(map(str, Answer_List)))
        region = {"Region": regions[i], "Distinct": Answer_List[i]}
        top_distinct_each_region.append(region)

    save_df = pd.DataFrame(top_distinct_each_region)
    save_df.to_csv("top_distinctive_words.csv", index=False)


if __name__ == "__main__":
    clean_files = cleanFiles()
    run_tfidf(clean_files)
