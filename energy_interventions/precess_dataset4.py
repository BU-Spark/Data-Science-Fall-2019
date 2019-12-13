import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

abslote_path = os.path.abspath('.')

dataset1_file = abslote_path + "/6ddcd912-32a0-43df-9908-63574f8c7e77.csv"
dataset2_file = abslote_path + "/fy19fullpropassess.csv"
headname_interv =['parcel_id','declared_valuation', 'total_fees']
headname_house =['PID','OWN_OCC']

pd.set_option('display.max_column', None)
pd.set_option('display.max_row', None)

def process_intervention_data_from_file(dataset_file):
    # filter the column
    raw_data = pd.read_csv(dataset_file)[headname_interv]
    raw_data['parcel_id']=raw_data['parcel_id'].replace({' ':np.nan})
    raw_data[['total_fees', 'declared_valuation']] = raw_data[['total_fees', 'declared_valuation']].replace(0, np.nan)
    # drop nan
    raw_data = raw_data.dropna()
    # put string type to int type
    raw_data['declared_valuation'] = raw_data['declared_valuation'].astype('int32')
    raw_data['total_fees'] = raw_data['total_fees'].astype('int32')
    # there are some negative number, put them to positive number
    raw_data['declared_valuation'] = raw_data['declared_valuation'].abs()
    raw_data['total_fees'] = raw_data['total_fees'].abs()
    raw_data['parcel_id'] = raw_data['parcel_id'].astype('int64')
    raw_data.info()
    return raw_data

def process_house_data_from_file(dataset_file):
    # filte the column
    raw_data = pd.read_csv(dataset_file)[headname_house]
    # rename the PID as parcel_id
    raw_data = raw_data.rename(columns={'PID': 'parcel_id'})
    raw_data.info()
    raw_data['OWN_OCC'].fillna('N', inplace=True)
    raw_data = raw_data.dropna()
    raw_data.info()
    return raw_data

def calculate_number_of_building(house_data):
    # calculate the number of intervention for each year
    group = house_data.groupby(['OWN_OCC']).count()
    group.reset_index(level=0, inplace=True)
    print(group)
    plt.bar(range(len(group['parcel_id'])), group['parcel_id'], tick_label=group['OWN_OCC'])
    plt.show()

def calculate_declared_valuation(total_data_set):
    # extract OWN_OCC and declared_valuation to analysis data
    pre_group = total_data_set[['OWN_OCC', 'declared_valuation']]
    # calculate the mean of declared_valuation for each year
    group = pre_group.groupby(['OWN_OCC']).mean()
    group.reset_index(level=0, inplace=True)
    print(group)
    plt.bar(range(len(group['declared_valuation'])), group['declared_valuation'], tick_label=group['OWN_OCC'])
    plt.show()

def calculate_total_fees(total_data_set):
    # extract OWN_OCC and total_fees to analysis data
    pre_group = total_data_set[['OWN_OCC', 'total_fees']]
    # calculate the mean of total_fees for each year
    group = pre_group.groupby(['OWN_OCC']).mean()
    group.reset_index(level=0, inplace=True)
    print(group)
    plt.bar(range(len(group['total_fees'])), group['total_fees'], tick_label=group['OWN_OCC'])
    plt.show()

df1 = process_intervention_data_from_file(dataset1_file)
df2 = house_data = process_house_data_from_file(dataset2_file)
# calculate_number_of_building(house_data)
newDf = pd.merge(df1,df2,on='parcel_id')
calculate_declared_valuation(newDf)
calculate_total_fees(newDf)