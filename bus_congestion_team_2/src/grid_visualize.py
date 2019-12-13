import os
import pickle
from datetime import timedelta, date
import pandas as pd
import numpy as np

from Grid import Region, Grid, get_grid_congestion_ratio, get_grid_congestion_ratio_24h

region = Region(42.70, -71.50, 42.10, -70.75)
cell_num = region.width * region.height

DATAPATH = "../bot/output/"


def get_grid_index(filename):
    df = pd.read_csv(filename)

    data_size = len(df)
    grid_index = np.zeros(data_size)
    for i in range(data_size):
        loc = (df["latitude"][i], df["longitude"][i])
        label = region.locate(loc)
        g = region.find_grid(label)
        try:
            grid_index[i] = g.label
        except:
            print("point out of bound: ", loc)

    return grid_index


def get_grid_index_24h(date):
    # date input is a string in format as "20191026"
    filenames = []
    for filename in os.listdir(DATAPATH):
        if date in filename:
            filenames.append(filename)

    grid_index_all = np.zeros(0)
    for filename in filenames:
        grid_index = get_grid_index(DATAPATH + filename)
        grid_index_all = np.append(grid_index_all, grid_index)

    return grid_index_all


def find_congestion_grids(filename, dt=None):
    if dt:
        grid_index = get_grid_index_24h(dt)
    else:
        grid_index = get_grid_index(filename)

    grid_dict = np.zeros(cell_num)  # record number of time the grid appears

    for i in grid_index:
        grid_dict[int(i)] += 1

    max_grid = max(grid_dict)

    grid_number_dots = np.zeros(int(max_grid) + 1)  # the dictionary of number of dots in grids -> number of such grids
    for i in grid_dict:
        grid_number_dots[int(i)] += 1

    num_nonzero_grids = cell_num - grid_number_dots[0]
    # print("number of nonzero grids: ", num_nonzero_grids)

    threshold = find_percentage(grid_number_dots, num_nonzero_grids, 0.01)
    # print("threshold is ", threshold)
    grid_congestion_dict = (grid_dict >= threshold)
    # print("number of congestion:", sum(grid_congestion_dict))

    return grid_congestion_dict


def find_percentage(grid_index_count, num_nonzero_grids, percentage=0.01):
    # num_nonzero_grids is the size of all number of nonempty grids
    # grid_index_count is the dictionary of number of dots in grids -> number of such grids
    percentlen = num_nonzero_grids * percentage
    count = 0
    for i in list(range(len(grid_index_count)))[::-1]:
        if count < percentlen:
            count += grid_index_count[i]
        else:
            return i


def find_congestion():
    all_grid_congestion_dict = np.zeros(cell_num)
    for file in os.listdir(DATAPATH):
        print(file)
        filename = DATAPATH + file
        # index_filename = "../bot/gridindex/" + filename[14:-4] + '_gridindex.data'
        grid_congestion_dict = find_congestion_grids(filename)
        all_grid_congestion_dict += grid_congestion_dict

    with open('grid_congestion.data', 'wb') as handle:
        pickle.dump(all_grid_congestion_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return all_grid_congestion_dict


def find_congestion_24h():
    all_grid_congestion_dict = np.zeros(cell_num)

    start_dt = date(2019, 10, 28)
    end_dt = date(2019, 11, 10)
    dates = []
    for dt in daterange(start_dt, end_dt):
        dates.append(dt.strftime("%Y%m%d"))

    for dt in dates:
        print(dt)
        grid_congestion_dict = find_congestion_grids(None, dt)
        all_grid_congestion_dict += grid_congestion_dict

    with open('grid_congestion_24h.data', 'wb') as handle:
        pickle.dump(all_grid_congestion_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return all_grid_congestion_dict


def get_index_high_ratio(rate=0.5):
    ratios = get_grid_congestion_ratio()
    high_ratios = (ratios >= rate)

    indices = []
    for i in range(len(high_ratios)):
        if high_ratios[i]:
            indices.append(i)
    return indices


def get_index_high_ratio_24h(rate=0.5):
    ratios = get_grid_congestion_ratio_24h()
    high_ratios = (ratios >= rate)

    indices = []
    for i in range(len(high_ratios)):
        if high_ratios[i]:
            indices.append(i)
    return indices


def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)


if __name__ == '__main__':
    # find_congestion()
    find_congestion_24h()
