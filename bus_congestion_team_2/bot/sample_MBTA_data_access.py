import requests
import json
import time
from datetime import datetime, timedelta
from functools import partial
import logging

# base url for mbta API
BASE_URL = 'https://api-v3.mbta.com/'

# replace with ur key
API_KEY = '69601055776b43039226b6882fbacaab'

# output header
HEADER = 'id,current_status,direction_id,latitude,longitude,updated_at,day,time_slot'

# the order to visit vehicle attributes
ORDER = ['current_status', 'direction_id', 'latitude', 'longitude', 'updated_at']

def get_all_routes():
	# bus_route_key = 'routes/?filter%5Btype%5D=3&fields%5Broute%5D=description,long_name,short_name,id'
	bus_route_key = 'routes/?filter%5Btype%5D=3&fields%5Broute%5D=id'

	bus_route_url = BASE_URL + bus_route_key
	json_fmt = requests.get(bus_route_url, headers={"x-api-key": API_KEY}).json()

	return json_fmt['data']

# @return value:
# 0 - Mon, ... , 6 - Sun
def get_day(timestamp, fmt):
	ts = datetime.strptime(timestamp, fmt)
	return ts.weekday()

# @return value:
# 0 - [00:00 - 00:59]
# 1 - [01:00 - 01:59]
# ...
# 23 - [23:00 - 23:59]
def get_timeslot(timestamp, fmt):
	ts = datetime.strptime(timestamp, fmt)
	return ts.hour if ts.hour >= 0 and ts.hour <= 23 else 0 # if 24:00 occur, take it as 00:00

# @vehicle - dict
# 	{'attributes':{'current_status': 'IN_TRANSIT_TO', 
#				 'direction_id': 0,
#				 'latitude': xxx - float num,
#			 	 'longitude': yyy - float num,
#			     'updated_at': '2019-10-25T19:05:40-04:00'},
#    'id': 'y1793'}
def parse_entry_to_csv(vehicle):
	res = vehicle['id']
	for key in ORDER:
		res = res + ',' + str(vehicle['attributes'][key])

	# add up two more attributes - day, time_slot(0 ~ 23, hr based)
	timestamp = vehicle['attributes']['updated_at'][:-6]
	day = get_day(timestamp, '%Y-%m-%dT%H:%M:%S')
	time_slot = get_timeslot(timestamp, '%Y-%m-%dT%H:%M:%S')

	res = res + ',' + str(day) + ',' + str(time_slot)

	# the return will be in form of 'id, current_status, direction_id, latitude, longitude, updated_at, day, time_slot'
	return res

def get_all_vehicles(routes, file_handler):
	vehicle_base = 'vehicles/?filter%5Broute%5D='
	vehicle_urls = [BASE_URL + vehicle_base + bus['id'] for bus in routes]

	for url in vehicle_urls:
		vehicles_in_route = requests.get(url, headers={"x-api-key": API_KEY}).json()
		for vehicle in vehicles_in_route['data']:
			file_handler.write(parse_entry_to_csv(vehicle) + '\n')

# partition routes into K parts to meet the maximum access limition at MBTA.com
def partition_routes(routes, k):
	res = [[] for _ in range(k)]
	for i, entry in enumerate(routes):
		cur = i % k
		res[cur].append(entry)

	return res

def construct_k_jobs(k):
	routes = get_all_routes()
	k_route_list = partition_routes(routes, k)

	jobs = [partial(get_all_vehicles, route) for route in k_route_list]

	return jobs

# @last - the hrs lasted to run this program
# @k - the number used to partition routes
# @intervals - the intervals between every request to MBTA.com
def runner(last, k, intervals=70):
	cur_job, times = 0, 0
	# create file with timestamp based on time slot
	file_handler = None

	jobs = construct_k_jobs(k)

	ending_time = datetime.now() + timedelta(hours=last)

	while datetime.now() < ending_time:

		now = datetime.now()
		YYMMDD = now.strftime('%Y%m%d')
		time_slot = get_timeslot(now.strftime('%Y%m%d - %H:%M:%S'), '%Y%m%d - %H:%M:%S')
		matched_file_name = 'result_' + YYMMDD + '_' + str(time_slot) + '.csv'

		if file_handler is None:
			file_handler = open(matched_file_name, 'w')
			file_handler.write(HEADER + '\n')

		elif file_handler.name != matched_file_name:
			file_handler.close() # close previous file object
			file_handler = open(matched_file_name, 'w')
			file_handler.write(HEADER + '\n')

		# print(f'run task #{cur_job} at: ' + str(time.ctime()))
		try:
			jobs[cur_job](file_handler)
		except Exception:
			logging.exception(f'task #{cur_job} failed at: ' + str(time.ctime()), exc_info=True)
		else:
			# print(f'task #{cur_job} ends at: ' + str(time.ctime()))
			pass
		time.sleep(intervals)
		cur_job = (cur_job + 1) % k
	
	try:
		file_handler.close()
	except:
		pass

if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

	# run hrs
	runner(last=24*14, k=3)
	
