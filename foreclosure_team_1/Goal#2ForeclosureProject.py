#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 12:41:09 2019

@author: khaiyevdayev
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file1 = "Abandoned_surveyed.csv"
file2 = "Abandoned_not_surveyed.csv"

#Openning both surveyed and not surveyed datasets
sur = pd.read_csv(file1, sep = ';')
not_sur = pd.read_csv(file2, sep = ';')

neigh1 = sur[['Parcel Neighborhood', "Parcel: BPDA Neighborhood"]]
neigh2 = not_sur[['Parcel Neighborhood', "Parcel: BPDA Neighborhood"]]
neighs = [neigh1,neigh2]
total_neigh = pd.concat(neighs)
total_neigh = total_neigh.dropna()

print(len(neigh1))
print(len(neigh2))
print(len(total_neigh))

prop_1 = total_neigh['Parcel Neighborhood'].value_counts()

prop_2 = total_neigh['Parcel: BPDA Neighborhood'].value_counts()

#Graphing the Neigborhoods by the amount of foreclosed properties
total_neigh['Parcel Neighborhood'].value_counts().plot(kind='barh', capstyle='projecting', 
                                                        hatch = '+', joinstyle='bevel', color='purple',
                                                       figsize=(20,20), title='The Number of Foreclosed/Abandoned Properties', label='Number of Foreclosed/Abandoned Properties', fontsize=15)

file_f = 'Foreclosure_Data.csv'
types = pd.read_csv(file_f, sep = ';')

housetype = types['Occupancy Description (fm Prcl)'].value_counts()

#Arrays with data from Boston Neighborhood Development for 2010
Neighborhoods=['Dorchester', 'Roxbury', 'Mattapan', 'East Boston', 'Hyde Park', 'Jamaic Plain','South Boston', 'Central',
              'Roslindale','Allston/Brighton','South End','West Roxbury','Fenway/Kenmore','Charlestown']
income_ = [45.807, 30.654, 42.164, 43.511, 53.474, 55.861,63.747, 65.662,62.702,52.362,51.870,71.066,32.509,83.926]
affordable_units = [0.14,.45,.19,.15,0.07, .26, .19, .16,.11,.13, .41,.1,.14,.30]
median_sale = [244.450,230, 215, 245, 239.9, 375,385,292.5,309,292.5,576,356.275,313.75,450]

#Median income for each neighborhood based on foreclosure frequency
plt.barh( Neighborhoods, income_, color='purple')
plt.xlabel('Median Income ($k)')

#Median residential sales prices for each neighborhood based on foreclosure frequency
plt.barh(Neighborhoods,median_sale, color='darkgreen')
plt.xlabel('Median Price for Apartment ($k)')

#Proportions of affordable houses for each neighborhood based on foreclosure frequency
plt.barh(Neighborhoods,affordable_units, color='orange')
plt.xlabel('Proportion of Affordable Units')

#Statistics for Top 5 and Lowest 5 Neighborhoods
#Attempting to compare how the median income and the median sales price of an apartment differ across the top 5 neighborgoods 
#with most foreclosure/abandoned units, from the lowest 5 neighborhoods with least foreclosure/abandoned units.

#First Income
bost = ['Boston']
bost_inc = [52.433]
bost_price = [292.5]
top_5 = ['Dorchester', 'Roxbury', 'Mattapan', 'East Boston', 'Hyde Park']
top_5_inc = [45.807, 30.654, 42.164, 43.511, 53.474]
top_5_price = [244.450,230, 215, 245, 239.9]

low_5 = ['Allston/Brighton','South End','West Roxbury','Fenway/Kenmore','Charlestown']
low_5_inc = [52.362,51.870,71.066,32.509,83.926]
low_5_price = [292.5,576,356.275,313.75,450] 

plt.figure(figsize=(15,10))
plt.barh(top_5, top_5_inc, color='skyblue', hatch='|')
for i, v in enumerate(top_5_inc):
    plt.text(v + 0.5, i, str(v), color='black', fontweight='bold')
plt.barh(bost,bost_inc, color='green', hatch='x')
for i, v in enumerate(bost_inc):
    plt.text(v + 0.5, i + 5, str(v), color='black', fontweight='bold')
plt.barh(low_5, low_5_inc, color='purple',hatch='|')
for i, v in enumerate(low_5_inc):
    plt.text(v + 0.5, i + 6, str(v), color='black', fontweight='bold')
plt.legend(["Top 5 Neighborhoods with Foreclosure","Boston","Least 5 Neighborhoods with Foreclosure"],loc=4)
plt.title('Comparison of Median Incomes within the Top 5 and Low 5 Neighborhoods')
plt.xlabel('Income ($k)')
filename = "median_income.png"
plt.savefig(filename)

#Then Median Sales Price
plt.figure(figsize=(15,10))
plt.barh(top_5,top_5_price, color='skyblue',hatch='|')
for i, v in enumerate(top_5_price):
    plt.text(v + 0.5, i, str(v), color='black', fontweight='bold')
plt.barh(bost, bost_price, color = 'green', hatch='x')
for i, v in enumerate(bost_price):
    plt.text(v + 0.5, i+5, str(v), color='black', fontweight='bold')
plt.barh(low_5,low_5_price,color='purple',hatch='|')
for i, v in enumerate(low_5_price):
    plt.text(v + 0.5, i + 6, str(v), color='black', fontweight='bold')
plt.legend(['Top 5 Neighborhoods with Foreclosure','Boston','Least 5 Neighborhoods with Foreclosure'],loc=4)
plt.title("Comparison of Median Residential Sales within the Top 5 and Low 5 Neighborhoods")
plt.xlabel("Price ($k)")
filename = "median_residential_prices.png"
plt.savefig(filename)