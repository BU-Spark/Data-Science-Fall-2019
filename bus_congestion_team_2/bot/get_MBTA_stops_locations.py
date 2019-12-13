import requests
import json

base_url = 'https://api-v3.mbta.com/'
bus_route_key = 'routes/?filter%5Btype%5D=3&fields%5Broute%5D=description,long_name,short_name,id'
stops = 'stops/?filter%5Broute%5D='
api_key = '69601055776b43039226b6882fbacaab'

# get all routes ID
bus_route_url = base_url + bus_route_key
resp = requests.get(bus_route_url)
json_fmt = resp.json()

# generate the urls for stops information of all routes
stops_urls = [base_url + stops + bus_route['id'] for bus_route in json_fmt['data']]

# input urls, get the latitude and longitude information
def getBoundary(urls):
    longitude = set()
    latitude = set()
    for i in range(42):
        if urls:
            url = urls.pop()
            stops_in_route = requests.get(url, headers={"x-api-key": api_key}).json()
            for stops in stops_in_route['data']:
                stop = stops['attributes']
                latitude.add(float(stop['latitude']))
                longitude.add(float(stop['longitude']))
        else:
            break
    return (latitude, longitude, urls)

# input boundary to filter routes
def routes_in_Boundary(urls, maxLa, maxLo, minLa, minLo):
    if urls:
        url = urls.pop()
        stops_in_route = requests.get(url, headers={"x-api-key": api_key}).json()
        n = 0
        alln = len(stops_in_route['data'])
        for stops in stops_in_route['data']:
            stop = stops['attributes']
            if minLa < stop['latitude'] < maxLa and minLo < stop['longitude'] < maxLo:
                n += 1
        if n // alln < 0.1:
            return url.split('5D=')[-1], urls
        return None, urls

maxLongitude, maxLatitude, minLongitude, minLatitude = -70.845879, 42.572979, -71.29081, 42.137852
la, lo = [], []
step = 0
address = []
latitude = []
for i in range(4):
    latitude, longitude, stops_urls = getBoundary(stops_urls)
    # print(latitude)
    la += latitude
    lo += longitude
    maxLatitude = max(la)
    minLatitude = min(la)
    maxLongitude = max(lo)
    minLongitude = min(lo)
    print(i, maxLatitude, maxLongitude, minLongitude, minLatitude)

# Previous result: maxlatitude: 42.587435  maxLongitude: -70.845016  minLongitude: -71.291173  minLatitude:42.106555
print(maxLatitude, maxLongitude, minLongitude, minLatitude)

routes_in_BPS = []
for i in range(168):
    print(i)
    route, stops_urls = routes_in_Boundary(stops_urls, maxLatitude, maxLongitude, minLatitude, minLongitude)
    if route:
        routes_in_BPS.append(route)
print(routes_in_BPS)