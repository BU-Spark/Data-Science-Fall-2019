# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 14:32:16 2019

@author: seanl
"""

import os

abslote_path = os.path.abspath('.')

dataset1_file = abslote_path + "/6ddcd912-32a0-43df-9908-63574f8c7e77.csv"
dataset2_file = abslote_path + "/fy19fullpropassess.csv"

headname_interv =['permitnumber','comments','issued_date','zip',
           'property_id','parcel_id','lat','long']
headname_house =['PID','GIS_ID','AV_LAND']
keyword_test = 'Solar|solar|heat pump|insulation|Insulation|gas stove|boiler|HVAC|Boiler|Furnace|furnace|Weather stripping|weather stripping'

import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.cluster import KMeans, AgglomerativeClustering
import matplotlib.pyplot as plt
import matplotlib
import random
colors = []
denotes = ['.',',','o','v','^','<','>','1','2','3',
           '4','8','s','p','*','h','H','+','x','d','D']

def create_color_option(colors):
    for name, hex in matplotlib.colors.cnames.items():
        colors.append(name) 
        
def process_intervention_data_from_file(dataset_file):
    raw_data = pd.read_csv(dataset_file)[headname_interv]
    # drop null
    raw_data['parcel_id']=raw_data['parcel_id'].replace({' ':np.nan})
    raw_data = raw_data.dropna(subset=['parcel_id','comments'])
    #raw_data['comments'] = raw_data['comments'].tolow()
    raw_data['parcel_id'] = raw_data['parcel_id'].astype('int64')
    #select intervention related sample 
    raw_data = raw_data[raw_data['comments'].str.contains(keyword_test)]
    raw_data.info()
    return raw_data

def process_house_data_from_file(dataset_file):
    raw_data = pd.read_csv(dataset_file)[headname_house]
    #fill null
    raw_data = raw_data.rename(columns={'PID':'parcel_id'})
    # drop duplicate samples
    raw_data = raw_data.drop_duplicates(keep='first')
    raw_data.info()
    return raw_data

def KPP_clustering(dataset,k):
    kpp = KMeans(
    n_clusters=k, init='k-means++',
    n_init=10, max_iter=300, 
    tol=1e-04, random_state=0
    )
    kpp.fit(dataset)
    return kpp

def KPP_elbow_plot(dataset,k):
    """
    Draw the elbow plot for kpp
    """
    distortions = []
    for i in range(1, k):
        kpp = KPP_clustering(dataset,i)
        distortions.append(kpp.inertia_)
    plt.plot(range(1, k), distortions, marker='o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.show()
    
def kpp_plot(kpp,dataset):
    num_centroids = len(kpp.cluster_centers_)
    #randomly choose the symbols and colos to plot 
    choose_color = random.sample(colors,num_centroids+1)
    choose_denote = random.sample(denotes,num_centroids+1)
    for i in range(num_centroids):
        i_label='cluster %d' % (i+1)
        plt.scatter(
                dataset[kpp.labels_ == i, 0], dataset[kpp.labels_ == i, 1],
                c=choose_color[i], marker=choose_denote[i],
                edgecolor='black', s=50,
                label=i_label
                )
    plt.scatter(
                kpp.cluster_centers_[:, 0], kpp.cluster_centers_[:, 1],
                c=choose_color[num_centroids], marker=choose_denote[num_centroids],
                edgecolor='red', s=150,
                label='centroid'
                )
    plt.legend(scatterpoints=1)
    plt.grid()
    plt.show()
    
df1 = process_intervention_data_from_file(dataset1_file)
df2 = process_house_data_from_file(dataset2_file)

newDf = pd.merge(df1,df2,on='parcel_id')
newDf = newDf.dropna(subset=['lat','long'])


dataset_s_loc = preprocessing.StandardScaler().fit_transform(newDf[['lat','long']])   
dataset_s_p = preprocessing.MinMaxScaler().fit_transform(newDf[['AV_LAND']])
print(dataset_s_loc)
print(dataset_s_p)
dataset= np.concatenate((dataset_s_loc,dataset_s_p),axis=1)
print(dataset)

kpp_clusters = 7
create_color_option(colors)
kpp = KPP_clustering(dataset,kpp_clusters)
kpp_plot(kpp,dataset)
res = pd.DataFrame(kpp.labels_,columns=['cluster'])
print(res.shape)
print(dataset.shape)
print(res['cluster'].value_counts())

dataset_df = pd.DataFrame(dataset,columns=['lat','long','price'])

dd = pd.concat([dataset_df,res],axis=1)
#print(dd)
print(dd.groupby('cluster')['price'].mean())