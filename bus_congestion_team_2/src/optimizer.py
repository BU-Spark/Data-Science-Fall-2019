from route_tracer import trace_street, substitue_route
from Grid import Region
import pandas as pd
from plot_bps import BPS_FILE, SCHOOL_FILE, clean_data, grainby, add_school_markers
from Grid import Region
import folium
import json

if __name__ == '__main__':
	f = open('../csv/GoogleAPIKey.txt', 'r')
	API_key = f.readline()
	f.close()

	school_locations = pd.read_csv(SCHOOL_FILE)
	bps_sensor = pd.read_csv(BPS_FILE)

	reg = Region(42.70, -71.50, 42.10, -70.75)
	reg.add_ratio()

	bps_sensor = clean_data(bps_sensor)
	routes = grainby(bps_sensor)
	for index, origin_route in enumerate(routes):

		if len(origin_route) > 300 or len(origin_route) < 15: continue

		base_map = folium.Map(location=(42.30, -71.05), zoom_start=13)
		folium.Polygon(origin_route, popup='bps route', color='blue', opacity=1).add_to(base_map)

		sts = trace_street(API_key, reg, origin_route)
		sts = [st for st in sts if not (st.begin_ptn == st.end_ptn)] # filter out single point street
		csts = [st for st in sts if st.has_congestion]

		subs_routes = substitue_route(csts)
		if len(subs_routes) == 0: continue

		add_school_markers(base_map, school_locations)

		for route in subs_routes:
			folium.Polygon(route, popup='optimized route', color='lightgreen', opacity=1).add_to(base_map)

		base_map.save(f'optimized/optimized_route_{index}.html')