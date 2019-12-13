import pandas as pd
import os
import folium
from folium.plugins import HeatMap
from datetime import datetime
from datetime import timedelta
from Grid import Region

# files = os.listdir(BASE_DIR)
# file_size = [(f, os.stat(f'{BASE_DIR}/{f}').st_size)for f in files]
# top_100 = sorted(file_size, key=lambda x:-x[1])

BPS_FILE = '../csv/bps_WB957.csv'
SCHOOL_FILE = '../csv/schools_locations.csv'
LINE_COLOR = 'blue'


def clean_data(bps_df):
	# clean out liers
	return bps_df[(bps_df.latitude >= 42.10) & (bps_df.latitude <= 42.70) \
		& (bps_df.longitude >= -71.50) & (bps_df.longitude <= -70.75)]


def add_school_markers(base_map, dataframe):
	for index, row in dataframe.iterrows():
		name = row['school name']
		frt, back = row['location'].split(',')

		lati, longi = float(frt[1:]), float(back[1:-1])
		folium.Marker((lati, longi), popup=name).add_to(base_map)

def grainby(dataframe, gap=600):
	res, cur = [], []

	prev_dt = None
	for index, row in dataframe.iterrows():
		dt = datetime.strptime(row.logtime, '%Y-%m-%d %H:%M:%S')

		if prev_dt and dt - prev_dt > timedelta(seconds=gap):
			res.append(cur)
			cur = []

		cur.append((row.latitude, row.longitude))
		prev_dt = dt

	if cur: res.append(cur)

	return res

def add_congested_area(base_map, congested_indexes):
	reg = Region(42.70, -71.50, 42.10, -70.75)
	for label in congested_indexes:
		grid = reg.find_grid(label)

		grid_center = ((grid.x + grid.m) / 2, (grid.y + grid.n) / 2)
		folium.Circle(grid_center, radius=70, color='red', fill_color='red').add_to(base_map)


def visualize(school_locations_df, bps_points, congested_indexes):
	base_map = folium.Map(location=(42.30, -71.05), zoom_start=13)

	folium.Polygon(bps_points, color=LINE_COLOR).add_to(base_map)

	# add up school marker
	add_school_markers(base_map, school_locations_df)
	
	# add up congested(red) area
	add_congested_area(base_map, congested_indexes)

	return base_map

if __name__ == '__main__':
	school_locations = pd.read_csv(SCHOOL_FILE)
	bps_sensor = pd.read_csv(BPS_FILE)

	index = 0
	bps_sensor = clean_data(bps_sensor)

	for points in grainby(bps_sensor):
		if len(points) < 50: continue # too few points can't be plotted in a line

		m = visualize(school_locations, points, [])
		m.save(f'plots/p-{index}.html')
		index+=1

		break