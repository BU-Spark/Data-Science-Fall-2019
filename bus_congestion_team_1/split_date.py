"""
@author: Zachary Hyman
"""

import pandas as pd
import os

def dataSort(df,date):
    '''Funciton to sort and export dataframes'''
    #Sort each individual date by bus entry
    df.sort_values(by=['vendorhardwareid','time'],inplace=True)
    #Delete date as no longer necessary
    del df['date']
    #Export to datafolder with date labeled csv
    df.to_csv(dataFolder + '/' + date + '_sortedbusdata.csv',index=False)
    return 0

def dataSplit(road_data_csv):
    '''Function used to split data by date'''
    #Import csv of all data into df object
    df = pd.read_csv(road_data_csv)
    #Split logtime of each entry into date and time columns
    df[['date', 'time']] = df.logtime.str.split(expand=True)
    #Delete logtime as no longer needed
    del df['logtime']
    #Sort table by date and find all unique dates
    df.sort_values(by=['date'], inplace=True)
    df.set_index(keys=['date'], drop=False, inplace=True)
    dates = df['date'].unique().tolist()
    #For each date create a clone of the database for the date and pass to dataSort()
    for dateIndex in dates:
        dfsplit = df.loc[df.date == dateIndex]
        dataSort(dfsplit,dateIndex)
    return 0



#Block to establish data export directory in current Unix environment
dataFolder = os.getcwd() + '/dataFolder'
if not os.path.exists(dataFolder):
    os.makedirs(dataFolder)

#IMPLIMENTATION
dataSplit('road_data.csv')


