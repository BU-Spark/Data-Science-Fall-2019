import googlemaps
import requests
import json
from plot_bps import BPS_FILE, SCHOOL_FILE, clean_data, grainby
from grid_index_set import get_rec_route, scoring
import pandas as pd
from Grid import Region
import folium

GRID_CONGESTED_THREASHOLD = 0.011538461538461539

class LocNode(object):
	def __init__(self, latitude_, longitude_):
		self.latitude = latitude_
		self.longitude = longitude_
		self.next = None
		self.prev = None

	def get_pair(self):
		return (self.latitude, self.longitude)

	def __eq__(self, other):
		return (self.latitude == other.latitude) and (self.longitude == other.longitude)

DUMMY_NODE = LocNode(-1, -1)

class Street(object):
	def __init__(self, name_):
		self.name = name_
		self.has_congestion = False
		self.route = list()
		self.begin_ptn = None
		self.end_ptn = None

	def __repr__(self):
		return f'<(Street: name=#{self.name}, begin=#{self.begin_ptn}), end=#{self.end_ptn}, congested=#{self.has_congestion}>'

	def __eq__(self, other):
		return self.name == other.name

	def get_route(self):
		if self.route: return self.route

		ptr = self.begin_ptn

		while not (ptr == self.end_ptn.next):
			if not ptr: break

			self.route.append(ptr.get_pair())
			ptr = ptr.next

		return self.route

	def get_two_ends(self):
		prev, nxt = self.begin_ptn, self.end_ptn # default to start, end point of current st
		if not (self.begin_ptn.prev == DUMMY_NODE): prev = self.begin_ptn.prev # not equals to dummy
		if self.end_ptn.next is not None: nxt = self.end_ptn.next

		return prev.get_pair(), nxt.get_pair()

def congested(board, latitude, longitude):
	label = board.locate((latitude, longitude))
	grid = board.find_grid(label)

	if grid.congestion_ratio > GRID_CONGESTED_THREASHOLD: return True
	return False

def google_req(api_key, latitude, longitude):
	url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}'
	resp = requests.get(url)
	st_name = None
	try:
		resp_json = resp.json()
		st_name = resp_json['results'][0]['address_components'][1]['long_name']
	except:
		print(f'ERR: google_req cant determine {latitude}, {longitude}')

	return st_name

def trace_street(api_key, region, points):

	sts = list()
	prev_st = None
	tail = dummy = DUMMY_NODE

	for index, val in enumerate(points):
		lati, longi = val
		
		node = LocNode(lati, longi)
		node.prev = tail
		tail.next = node
		tail = node

		name = google_req(api_key, lati, longi)

		if prev_st is None or prev_st != name:
			st = Street(name)
			st.begin_ptn = node
			st.end_ptn = node

			# push new st to list
			sts.append(st)
			prev_st = name
		else:
			sts[-1].end_ptn = node

		if congested(region, lati, longi): sts[-1].has_congestion = True

	return sts

def substitue_route(sts):
	all_subs = list()
	for st in sts:
		cur_route = st.get_route()
		score = scoring(cur_route)
		A, B = st.get_two_ends()

		found, route = get_rec_route(A, B, score)
		if found: all_subs.append(route)

	return all_subs


if __name__ == '__main__':
	f = open('../csv/GoogleAPIKey.txt', 'r')
	API_key = f.readline()
	f.close()

	school_locations = pd.read_csv(SCHOOL_FILE)
	bps_sensor = pd.read_csv(BPS_FILE)

	reg = Region(42.70, -71.50, 42.10, -70.75)
	reg.add_ratio()

	bps_sensor = clean_data(bps_sensor)
	for pnts in grainby(bps_sensor):
		sts = trace_street(API_key, reg, pnts)
		bps_points = list()
		for st in sts:
			bps_points.append(st.begin_ptn.get_pair())
			if not (st.begin_ptn == st.end_ptn):
				bps_points.append(st.end_ptn.get_pair())

		base_map = folium.Map(location=(42.30, -71.05), zoom_start=13)
		folium.Polygon(bps_points, color='red').add_to(base_map)

		base_map.save('route_tracer.html')
		break
