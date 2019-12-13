# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 23:41:16 2019

@author: harki
"""

import pandas as pd
import os


def time_to_dist(total_time, total_distance):
    """calculates the time to distance ratio, if total_distance is 0, then it returns 0"""
    if total_distance == 0:
        return 0
    else:
        return total_time/total_distance

def process_data(df, summary_df, date, bus, route_num):
    route = []
    total_distance = 0.0
    total_time = 0.0
    idle_time = 0.0
    for i in range(len(df)):
        #Run block if not the first record
        if i != 0:
            if df.loc[i, 'road_name'] != df.loc[i-1, 'road_name']:
                route += [df.loc[i, 'road_name']]
        #Run block if the first record
        else:
            route += [df.loc[0, 'road_name']]
        total_distance += df.loc[i, 'distance_travelled']
        total_time += df.loc[i, 'time_elapsed']
        #Run block if avg speed = 0
        if df.loc[i, 'avg_speed'] == 0:
            idle_time += df.loc[i, 'time_elapsed']
    #Run block if route is an empty list
    if route == []:
        start_road = ''
        end_road = ''
    #Run block if route is not an empty list
    else:
        start_road = route[0]
        end_road = route[-1]
    route_len = len(route)
    time_to_dist_ratio = time_to_dist(total_time, total_distance) #calculates the time-to-distance ratio
    summary_df = summary_df.append(pd.Series([date, bus, route_num, route, route_len, start_road, end_road, total_distance, total_time, idle_time, time_to_dist_ratio], index=summary_df.columns), ignore_index=True)
    return summary_df

def implement(directory_path, export_file_path):
    count = 0
    summary_df = pd.DataFrame(columns=['Date', 'Bus', 'Route_num', 'Route_road_lst', 'route_len', 'Start_road', 'end_road', 'total_distance', 'total_time', 'idle_time', 'time_to_dist'])
    #Loops through the folder in the directory_path
    for folder in os.listdir(directory_path):
        date = os.path.basename(folder)[11:] #extracts date from the folder name
        path = directory_path+folder+'/' #creates the path to the files
        #Loops through the files in path
        for file in os.listdir(path):
            filepath = path+file
            count += 1
            filename = os.path.basename(file)[:-4] #extracts filename
            route_num = filename[13] #extracts the route number of the bus
            bus = filename[15:] #extracts the bus name
            df = pd.read_csv(filepath) 
            summary_df = process_data(df, summary_df, date, bus, route_num)
    export_file_name = export_file_path+'Q2_results.csv'
    summary_df.to_csv(export_file_name)  #exports the results in summary_df to a csv file

export_file_path = input("Enter the Export Path for the results:")
directory_path = input("Enter Directory Path for folder which contains the folders of csv files from Q1:")
implement(directory_path, export_file_path)