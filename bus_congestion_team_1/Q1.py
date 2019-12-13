# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 22:13:09 2019

@author: harki
"""

import pandas as pd
import math
import datetime as dt
import os

directory_path = input("dataset/")
export_file_path = input("Q1_results")

def creating_route_label(df):
    """creating label for routes"""
    label = 1
    for i in range(len(df)):
        if i == df['time'].count()-1:
            df.loc[i, 'route_label'] = label
            break
        else:
            #creates a new label if the time difference between the current and previous record is greater than 1 hr
            if int(df.loc[i+1, 'time'][:2]) - int(df.loc[i, 'time'][:2]) > 1:
                label += 1
                df.loc[i, 'route_label'] = label
            else:
                df.loc[i, 'route_label'] = label
    return df

def splitting_routes(df):
    """splits into multiple dataframes (stored in a dictionary) based on the route label"""
    UniqueRoutes = df.route_label.unique()
    dfDict = {elem: pd.DataFrame for elem in UniqueRoutes}
    for key in dfDict.keys():
        dfDict[key] = df[:][df.route_label == key]
    return dfDict

def distance(start_lat, start_lon, end_lat, end_lon):
    """calculates distance in miles"""
    radius = 3958.8 #in miles
    dlat = math.radians(end_lat-start_lat)
    dlon = math.radians(end_lon-start_lon)
    a = math.sin(dlat/2)*math.sin(dlat/2) + math.cos(math.radians(start_lat)) * math.cos(math.radians(end_lat)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

def time(start_time, end_time):
    """calculates time in minutes"""
    start_dt = dt.datetime.strptime(start_time, '%H:%M')
    end_dt = dt.datetime.strptime(end_time, '%H:%M')
    diff = end_dt - start_dt
    return (diff.seconds/60)+1 #returns time interval in minutes

def average_speed(distance, time):
    """calculates average speed"""
    return distance/time

def speed_percentage(avg_speed, speed_limit):
    """calculates speed percentage based on speed limit of the road"""
    return (avg_speed/speed_limit)*100

def mph_to_milespmin(speed):
    """converts speed from miles per hour to miles per min"""
    return speed*0.0167

def processing_data(df, summary_df):
    """processes the data"""
    #Step 1: Replace all 0s in speedlimit column to either the mode of the column or 30 mph (if mode=0)
    mode = df['speedlimit'].mode().array[0]
    if mode != 0:
        df['speedlimit'] = df['speedlimit'].replace(0, mode)
    else:
        df['speedlimit'] = df['speedlimit'].replace(0, 30)
    #Step 2: assigning the 1st record as start_lat, start_lon, start_time, road_name and speed_limit
    start_lat = df.loc[0, 'latitude']
    start_lon = df.loc[0, 'longitude']
    start_time = df.loc[0, 'time']
    road_name = df.loc[0, 'road_name']
    speed_limit = df.loc[0, 'speedlimit']
    #Step 3: Starting loop
    for i in range(1, len(df)):
        #Run block if 'road_name' is the same as the road_name in ith record
        if road_name == df.loc[i, 'road_name']:
            #print("same road name", i)
            #Run block if time difference between current and previous record is less than or equal to 2
            if time(df.loc[i-1,'time'], df.loc[i, 'time']) <= 2:
                #print("time diff less than 2")
                #Run block if 'speed_limit' is different from speedlimit of the ith record
                if speed_limit != df.loc[i, 'speedlimit']:
                    #print("diff speed")
                    speed_limit = min(speed_limit, df.loc[i, 'speedlimit']) #chose lower speed_limit
                #Run block if i is last record in dataframe
                if i == df['road_name'].count() - 1:
                    #print("last record", i)
                    end_lat = df.loc[i, 'latitude']
                    end_lon = df.loc[i, 'longitude']
                    end_time = df.loc[i, 'time']
                    speed = df.loc[i, 'speed']
                    summary_df = road_travelled(start_lat, start_lon, start_time, end_lat, end_lon, end_time, speed, speed_limit, road_name, summary_df)
                    break
            #Run block if time different between current and previous record is more than 2
            else:
                #print("time diff greater than 2")
                #assigning previous record data as end_lat, end_lon & end_time
                end_lat = df.loc[i-1, 'latitude']
                end_lon = df.loc[i-1, 'longitude']
                end_time = df.loc[i-1, 'time']
                speed = df.loc[i-1, 'speed']
                #calculating distance travelled, total time elapsed, average speed and speed percentage
                summary_df = road_travelled(start_lat, start_lon, start_time, end_lat, end_lon, end_time, speed, speed_limit, road_name, summary_df)
                #assigning current record as start_lat, start_lon, start_time, road_name and speed_limit
                start_lat = df.loc[i, 'latitude']
                start_lon = df.loc[i, 'longitude']
                start_time = df.loc[i, 'time']
                road_name = df.loc[i, 'road_name']
                speed_limit = df.loc[i, 'speedlimit']
                #Run block if i is last record in dataframe
                if i == df['road_name'].count() - 1:
                    #print("last record", i)
                    end_lat = df.loc[i, 'latitude']
                    end_lon = df.loc[i, 'longitude']
                    end_time = df.loc[i, 'time']
                    speed = df.loc[i, 'speed']
                    summary_df = road_travelled(start_lat, start_lon, start_time, end_lat, end_lon, end_time, speed, speed_limit, road_name, summary_df)
                    break
        #Run block if 'road_name' is not the same as the road_name in record
        else:
            #print("diff road name", i)
            #assigning previous record data as end_lat, end_lon & end_time
            end_lat = df.loc[i-1, 'latitude']
            end_lon = df.loc[i-1, 'longitude']
            end_time = df.loc[i-1, 'time']
            speed = df.loc[i-1, 'speed']
            #calculating distance travelled, total time elapsed, average speed and speed percentage
            summary_df = road_travelled(start_lat, start_lon, start_time, end_lat, end_lon, end_time, speed, speed_limit, road_name, summary_df)
            #assigning current record as start_lat, start_lon, start_time, road_name and speed_limit
            start_lat = df.loc[i, 'latitude']
            start_lon = df.loc[i, 'longitude']
            start_time = df.loc[i, 'time']
            road_name = df.loc[i, 'road_name']
            speed_limit = df.loc[i, 'speedlimit']
            #Run block if i is last record in dataframe
            if i == df['road_name'].count() - 1:
                #print("last record", i)
                end_lat = df.loc[i, 'latitude']
                end_lon = df.loc[i, 'longitude']
                end_time = df.loc[i, 'time']
                speed = df.loc[i, 'speed']
                summary_df = road_travelled(start_lat, start_lon, start_time, end_lat, end_lon, end_time, speed, speed_limit, road_name, summary_df)
                break
            
    return summary_df
    
def road_travelled(start_lat, start_lon, start_time, end_lat, end_lon, end_time, speed, speed_limit, road_name, summary_df):
    """calculates summary statistics for the road travelled"""
    #print(start_lat, start_lon, start_time, end_lat, end_lon, end_time, speed_limit, road_name)
    distance_travelled = distance(start_lat, start_lon, end_lat, end_lon)
    #print(distance_travelled)
    time_elapsed = time(start_time, end_time)
    #print(time_elapsed)
    if start_lat == end_lat and start_lon == end_lon:
        avg_speed = mph_to_milespmin(speed)
    else:
        avg_speed = average_speed(distance_travelled, time_elapsed)
    speed_limit_in_milespmin = mph_to_milespmin(speed_limit)
    speed_perct = speed_percentage(avg_speed, speed_limit_in_milespmin)
    #print(speed_perct)
    summary_df = summary_df.append(pd.Series([road_name, speed_limit_in_milespmin, distance_travelled, time_elapsed, avg_speed, speed_perct], index=summary_df.columns), ignore_index=True)
    #print(summary_df.count())
    return summary_df

def implement(directory_path, export_file_path):
    #Loops through the files in the directory path
    for file in os.listdir(directory_path):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"): #checks if the file is in csv format
            df = pd.read_csv(directory_path+filename)
            df = creating_route_label(df)
            dfDict = splitting_routes(df)
            for key in dfDict.keys():
                temp_df = dfDict[key]
                temp_df = temp_df.reset_index()
                summary_df = pd.DataFrame(columns=['road_name', 'speedlimit', 'distance_travelled', 'time_elapsed', 'avg_speed', 'speed_percentage'])
                summary_df = processing_data(temp_df, summary_df)
                export_file_name = export_file_path+'Summary_Route'+str(int(key))+'_'+(os.path.basename(filename))
                summary_df.to_csv(export_file_name)


implement(directory_path, export_file_path)