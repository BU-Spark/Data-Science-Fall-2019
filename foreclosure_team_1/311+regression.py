import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import numpy as np
# Iteratively read files
import pandas as pd
from sklearn.linear_model import LogisticRegression

    
def process311():
    Aban_Last_Yr = pd.read_csv('Aban_Last_Yr.csv')
    Preliminary = pd.read_csv('Preliminary.csv')
    data_311 = pd.read_csv('311.csv')
    
    data_311 = data_311.iloc[ : 10000, : ]
    
    dict_311 = {}
    dict_pre = {}
    dict_311_case_title = {}
    dict_311_subject = {}
    dict_311_reason = {}
    
    top_foreclosure = ["02128", "02136", "02127", "02131"]
    bottom_foreclosure = ["02120", "02114", "02122", "02110"]
    
    total = 0
    for index, row in data_311.iterrows(): 
        location = row["location"]
        zip_code = location[ -5 : ]
        case_title = row['case_title']
        if zip_code in bottom_foreclosure:
            total = total + 1
            if case_title in dict_311_case_title:
                dict_311_case_title[case_title] = dict_311_case_title[case_title] + 1
            else:
                dict_311_case_title[case_title] = 1
                
    for key in dict_311_case_title:
        dict_311_case_title[key] = round(dict_311_case_title[key] / total, 3)
    
    
    for index,item in data_311["location"].iteritems(): 
        zip_code = item[ -5 : ]
        if zip_code in dict_311:
            dict_311[zip_code] = dict_311[zip_code] + 1
        else:
            dict_311[zip_code] = 0
#    
    for index,item in Preliminary["Parcel: Parcel ZIP"].iteritems(): 
        zip_code = '0' + str(item)
        if zip_code in dict_pre:
            dict_pre[zip_code] = dict_pre[zip_code] + 1
        else:
            dict_pre[zip_code] = 0
    
    for index,item in Aban_Last_Yr["Parcel: Parcel ZIP"].iteritems(): 
        zip_code = '0' + str(item)
        if zip_code in dict_pre:
            dict_pre[zip_code] = dict_pre[zip_code] + 1
        else:
            dict_pre[zip_code] = 0
    
    
    dict_311 = sorted(dict_311.items(), key = lambda x:x[1])
    dict_pre = sorted(dict_pre.items(), key = lambda x:x[1])
    dict_311_case_title = sorted(dict_311_case_title.items(), key = lambda x:x[1])
#    dict_311_subject = sorted(dict_311_subject.items(), key = lambda x:x[1])
#    dict_311_reason = sorted(dict_311_reason.items(), key = lambda x:x[1])

    print(dict_311)
    print(dict_pre)
    
    dict_311_case_title = dict_311_case_title[-10 : ]
    dict_311_case_title = list(reversed(dict_311_case_title))
    plt.figure(figsize=(8, 6), dpi=80)
    N = 10
    titles = []
    values = []
    
    for item in dict_311_case_title:
        if item[0] == ' ' or item[0] == ' MA  ': 
            continue
        titles.append(item[0][:7])
        values.append(item[1])
    
    print(len(titles))
        
    index = np.arange(N)
    width = 0.45
    
    color=["#87CEFA", "#008B8B", "#2E8B57", "#C0FF3E", "#FFEC8B", 
           "#FFC125", "#8B658B", "#FF6A6A", "#FF1493", "#1C1C1C", "#9A32CD", "#828282", "#F0FFF0"]
    
    p2 = plt.bar(index, values, width, label="num", color=[color[0], color[2], 
                                                           color[1], color[6], 
                                                           color[3], color[4], 
                                                           color[10], color[11],
                                                           color[7], color[12]])
    
    plt.xlabel('factors')
    plt.ylabel('percentage')
    plt.title('Statistics for bottom foreclosure areas')
    plt.xticks(index, titles)
    plt.show()
    
    
def linearRegression():
    data_foreclosure = pd.read_excel('Foreclosure_Data.xlsx')
    data_foreclosure = data_foreclosure.iloc[:,37:]
    
    data_311 = pd.read_csv('311.csv')
    data_311 = data_311.iloc[ : 500, 26:28 ]
    
    
    data_foreclosure = data_foreclosure.rename(columns={"Parcel: X Coordinate": "longitude", "Parcel: Y Coordinate": "latitude"})
    
#    foreclosure["Parcel: X Coordinate", "Parcel: Y Coordinate"]
    for i in range(0,419,1):
        for j in range(0,2,1):
            data_foreclosure.ix[i][j]=float('%.4f' %data_foreclosure.ix[i][j])
    
    foreclosed = [1] * 419
    data_foreclosure['foreclosed'] = foreclosed
    data_foreclosure = data_foreclosure.drop_duplicates()
    
#    foreclosed_coordinates = set()
    
#    for index, row in data_foreclosure.iterrows(): 
#        foreclosed_coordinates.add(str(row["Parcel: X Coordinate"]) + str(row["Parcel: Y Coordinate"]))
    
    foreclosed = [0] * 500
    data_311['foreclosed'] = foreclosed
    data_311 = data_311.drop_duplicates()
    
    concat_data = pd.concat([data_foreclosure, data_311], axis=0, ignore_index=True)
    
#    for index, row in data_311.iterrows():
#        coordinates = str(["latitude"]) + str(["longitude"])
#        if(coordinates in foreclosed_coordinates):
#            foreclosed_coordinates.add()
    
    
    concat_data = concat_data.drop_duplicates(["latitude", "longitude"], keep = 'first')
    X_train, X_test, y_train, y_test = train_test_split(concat_data[["latitude", "longitude"]], concat_data["foreclosed"], test_size = 0.20)
    
    clf = LogisticRegression()
    model = clf.fit(X_train, y_train)
    pred = model.predict(X_test)
    
    cm = confusion_matrix(y_test,pred)
    print(cm)
    
    print("Accuracy is {}".format(model.score(X_test, y_test)))
    
        
if __name__== "__main__":
    linearRegression()