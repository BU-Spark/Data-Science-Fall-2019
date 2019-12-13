import pandas as pd
import numpy as np

GROUP_BY_OUTPUT_DIR = '../csv/bps-groupby-vendor'
BPS_FILE_PATH = '../csv/18.07.11 Combined Abridged Road Speed Export.csv'

# group BPS data by vendorId, then sort them by timestamp
def bps_groupby_sort_tocsv(bps_df):
	keys = bps_df.vendorhardwareid.unique()
	for vid in keys:
		tmp = bps_df[bps_df['vendorhardwareid'] == vid]
		tmp.sort_values(by=['logtime'], inplace=True)
		tmp.reset_index(inplace=True, drop=True)
		tmp.to_csv(GROUP_BY_OUTPUT_DIR + f'/bps_{vid}.csv', index=False)

# identify the target region around Boston
# divide the region into bunch of grids
# fill the grids with scraped data points from MBTA portal
# def fill_out_grids(grids, MBTA_df):


if __name__ == '__main__':
	bps_df = pd.read_csv(BPS_FILE_PATH, index_col=0)
	# bps_groupby_sort_tocsv(bps_df)
	bin_values = np.arange(start=37.7, stop=46.6, step=0.1)
	bps_df.latitude.hist(bins=bin_values, figsize=[14,6])