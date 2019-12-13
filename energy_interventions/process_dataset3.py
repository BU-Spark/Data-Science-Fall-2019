import os

abslote_path = os.path.abspath('.')

dataset1_file = abslote_path + "/6ddcd912-32a0-43df-9908-63574f8c7e77.csv"
dataset2_file = abslote_path + "/fy19fullpropassess.csv"

headname_interv = ['permitnumber', 'comments', 'issued_date', 'zip',
                   'property_id', 'parcel_id', 'lat', 'long']
headname_house = ['PID', 'GIS_ID', 'AV_LAND']
keyword_test = 'Solar|solar|heat pump|insulation|Insulation|gas stove|boiler|HVAC|Boiler|Furnace|furnace|Weather stripping|weather stripping'

import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.cluster import KMeans, AgglomerativeClustering
import matplotlib.pyplot as plt
import matplotlib
import random

colors = []
denotes = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3',
           '4', '8', 's', 'p', '*', 'h', 'H', '+', 'x', 'd', 'D']


def create_color_option(colors):
    for name, hex in matplotlib.colors.cnames.items():
        colors.append(name)


def process_intervention_data_from_file(dataset_file):
    raw_data = pd.read_csv(dataset_file)[headname_interv]
    # drop null
    raw_data['parcel_id'] = raw_data['parcel_id'].replace({' ': np.nan})
    raw_data = raw_data.dropna(subset=['parcel_id', 'comments'])
    # raw_data['comments'] = raw_data['comments'].tolow()
    raw_data['parcel_id'] = raw_data['parcel_id'].astype('int64')
    # select intervention related sample
    raw_data = raw_data[raw_data['comments'].str.contains(keyword_test)]
    raw_data.info()
    return raw_data


def process_house_data_from_file(dataset_file):
    raw_data = pd.read_csv(dataset_file)[headname_house]
    # fill null
    raw_data = raw_data.rename(columns={'PID': 'parcel_id'})
    # drop duplicate samples
    raw_data = raw_data.drop_duplicates(keep='first')
    raw_data.info()
    return raw_data


def judging_solar_df(dataset_file):
    solar_df = dataset_file[dataset_file['comments'].str.contains('Solar|solar')]
    solar_df['judging'] = solar_df.comments.apply(lambda x: 'solar' if 'Solar' or "solar" in x else 0)
    return solar_df


def judging_heatpump_df(dataset_file):
    heatpump_df = dataset_file[dataset_file['comments'].str.contains('heat pump')]
    heatpump_df['judging'] = heatpump_df.comments.apply(lambda x: 'heatpump' if 'heat pump' in x else 0)
    return heatpump_df


def judging_insulation_df(dataset_file):
    insulation = dataset_file[dataset_file['comments'].str.contains('insulation|Insulation')]
    insulation['judging'] = insulation.comments.apply(lambda x: 'insulation' if 'insulation' or "Insulation" in x else 0)
    return insulation


def judging_HVAC_df(dataset_file):
    HVAC_df = dataset_file[dataset_file['comments'].str.contains('HVAC')]
    HVAC_df['judging'] = HVAC_df.comments.apply(lambda x: 'HVAC' if 'HVAC' in x else 0)
    return HVAC_df


def judging_boiler_df(dataset_file):
    boiler_df = dataset_file[dataset_file['comments'].str.contains('boiler|Boiler')]
    boiler_df['judging'] = boiler_df.comments.apply(lambda x: 'boiler' if 'boiler' or "Boiler" in x else 0)
    return boiler_df

def judging_stove_df(dataset_file):
    stove_df = dataset_file[dataset_file['comments'].str.contains('gas stove')]
    stove_df['judging'] = stove_df.comments.apply(lambda x: 'gasstove' if 'gas stove' in x else 0)
    return stove_df


def judging_furnance_df(dataset_file):
    furnace_df = dataset_file[dataset_file['comments'].str.contains('Furnace|furnace')]
    furnace_df['judging'] = furnace_df.comments.apply(lambda x: 'furnace' if 'furnace' or "Furnace" in x else 0)
    return furnace_df


def judging_weather_df(dataset_file):
    weather_df = dataset_file[dataset_file['comments'].str.contains('Weather stripping|weather stripping')]
    weather_df['judging'] = weather_df.comments.apply(lambda x: 'weather stripping' if 'weather stripping' or "Weather stripping" in x else 0)
    return weather_df


def calculate_declared_valuation(total_data_set):
    # extract YR_BUILT and declared_valuation to analysis data
    pre_group = total_data_set[['YR_BUILT', 'declared_valuation']]
    # calculate the mean of declared_valuation for each year
    group = pre_group.groupby(['YR_BUILT']).mean()
    group.reset_index(level=0, inplace=True)
    print(group)
    plt.plot(group['declared_valuation'], group['YR_BUILT'])
    plt.show()


df1 = process_intervention_data_from_file(dataset1_file)
df2 = process_house_data_from_file(dataset2_file)
newDf = pd.merge(df1,df2,on='parcel_id')
# print(newDf)
solar_df = judging_solar_df(newDf)
heatpump_df = judging_heatpump_df(newDf)
HVAC_df = judging_HVAC_df(newDf)
weather_df = judging_weather_df(newDf)
furnance_df = judging_furnance_df(newDf)
stove_df = judging_stove_df(newDf)
boiler_df = judging_boiler_df(newDf)
insulation_df = judging_insulation_df(newDf)
# print(solar_df)
size_list = [len(solar_df),
             len(heatpump_df),
             len(HVAC_df),
             len(weather_df),
             len(furnance_df),
             len(stove_df),
             len(boiler_df),
             len(insulation_df)]
print(size_list)
namelist = ['solar', 'heatpump', 'HVAC', 'weather', 'furnance', 'stove', 'boiler', 'insulation']
plt.bar(namelist, size_list)
plt.xlabel('name of intervention')
plt.ylabel('number')
plt.title('number of intervention')
plt.show()
# judged_df = pd.concat([solar_df,
#                        heatpump_df,
#                        HVAC_df,
#                        weather_df,
#                        furnance_df,
#                        stove_df,
#                        boiler_df,
#                        insulation_df])
# print(judged_df['judging'])
# print(judged_df)