# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 17:16:27 2019

@author: harki
"""

import pandas as pd
import os

def create_dataframe(filename): 
    """reads data from a csv file into a dataframe"""
    data = pd.read_csv(filename)
    return data

def remove_null_values(dataframe):
    """removes rows or columns containing null values from a dataframe"""
    dataframe.dropna()
    
def split_individual_bus_data(dataframe):
    """splits the data frame into multiple dataframes based on individual buses and returns 
       in the form of dictionary of dataframes"""
    UniqueBuses = dataframe.vendorhardwareid.unique()
    DataFrameDict = {elem : pd.DataFrame for elem in UniqueBuses}
    for key in DataFrameDict.keys():
        DataFrameDict[key] = dataframe[:][dataframe.vendorhardwareid == key]
    return DataFrameDict, UniqueBuses

def remove_seconds(DataFrameDict, UniqueBuses):
    """removes the seconds from the time column from each dataframe in DataFrameDict"""
    start, stop = 0, 5
    for key in UniqueBuses:
        DataFrameDict[key]['time'] = DataFrameDict[key]['time'].astype(str)
        DataFrameDict[key]["time"] = DataFrameDict[key]['time'].str.slice(start, stop)
    return DataFrameDict

def remove_time_duplicates(DataFrameDict, UniqueBuses):
    """Removes time duplicates"""
    for key in UniqueBuses:
        DataFrameDict[key] = DataFrameDict[key].drop_duplicates(subset='time', keep='last')
    return DataFrameDict

def get_length(DataFrameDict, UniqueBuses):
    """get the length of all dataframes in DataFrameDict"""
    length = 0
    for key in UniqueBuses:
        length += len(DataFrameDict[key].index)
    return length

def export_to_csv(DataframeDict, UniqueBuses, filepath):
    """exports data to  csv"""
    for key in UniqueBuses:
        DataframeDict[key].to_csv(filepath)

def implement(directory_path, export_filepath):
    """Takes directory path containing files containing Data splits the data based on individual buses, truncates seconds and removes time duplicates and exports data to export_filepath"""
    for file in os.listdir(directory_path):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            df = create_dataframe(filename)
            remove_null_values(df)
            DataFrameDict, UniqueBuses = split_individual_bus_data(df)
            DataFrameDict = remove_seconds(DataFrameDict, UniqueBuses)
            DataFrameDict = remove_time_duplicates(DataFrameDict, UniqueBuses)
            export_to_csv(DataFrameDict, UniqueBuses, export_filepath)

directory_path = input("Enter the directory path for the folder with the csv files:")
export_filepath = input("Enter the export path for the results:")

implement(directory_path, export_filepath)