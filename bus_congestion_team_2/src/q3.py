import googlemaps
import requests
import json
from plot_bps import BPS_FILE, SCHOOL_FILE, clean_data, grainby
import pandas as pd
from Grid import Region
import folium

def score_route(board, route_pnts):

	grids_met = set()
	for pnt in route_pnts:
		label = board.locate(pnt)
		grids_met.add(label)

	N = len(grids_met)
	scores = 0
	for label in grids_met:
		g = board.find_grid(label)
		scores += g.congestion_ratio

	return scores / N


if __name__ == '__main__':
	school_locations = pd.read_csv(SCHOOL_FILE)
	bps_sensor = pd.read_csv(BPS_FILE)

	reg = Region(42.70, -71.50, 42.10, -70.75)
	reg.add_ratio()

	bps_sensor = clean_data(bps_sensor)
	scores = [(pnts, score_route(reg, pnts)) for pnts in grainby(bps_sensor)]

	base_map = folium.Map(location=(42.30, -71.05), zoom_start=13)

	idling_route = min(scores, key=lambda x: x[1])
	busy_route = max(scores, key=lambda x: x[1])

	folium.Polygon(idling_route[0], color='blue', popup='most idling', opacity=1).add_to(base_map)
	folium.Polygon(busy_route[0], color='red', popup='most busy', opacity=1).add_to(base_map)

	base_map.save('q3.html')