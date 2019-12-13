# Importing required libraries 

import requests 
import json 

import pandas as pd 
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from uszipcode import SearchEngine

# calcuate driving distance between 2 points unit in miles
def calculateDistance(lat1, lng1, lat2, lng2):
    url = 'http://router.project-osrm.org/route/v1/driving/'
    pos1 = str(lng1) +',' + str(lat1)
    pos2 = str(lng2) +',' + str(lat2)
    locations = pos1 +';'+pos2
    response = requests.get(url+locations)
    data = json.loads(response.content)
    if response.status_code == 200:
        return data['routes'][0]['distance']*0.000621371 # in miles
    else:
        return 0
# Tests
calculateDistance(42.1417653,-71.2494985,42.34735,-71.075727)
calculateDistance(42.34735,-71.075727, 42.1417653,-71.2494985)
def convertZip(zipStr):
    """
    convert '2138.0' to '02138'
    """
    zipCode = ''
    if zipStr is not None:
        if '.' in zipStr:
            zipCode = '0' + zipStr[:4]
    return zipCode

def do_geocode(address, locator, loop=0):
    try:
        return locator.geocode(address)
    except GeocoderTimedOut:
        if loop >=5:
            return None
        time.sleep(5)
        return do_geocode(address, locator, loop+1)
    
    
def findLatitude_Longitude(street, zipCode, state, country, locator, searchEngine):
    city = searchEngine.by_zipcode(zipCode).major_city
    fullAddress= street+', '+ city +', '+ state+', '+ zipCode +', '+country
    print(fullAddress)
    location = do_geocode(fullAddress, locator)
    if not location:
        return (None,None)
   # print(location.latitude, location.longitude)
    return (location.latitude, location.longitude)

# =============================================================================
# read places csv file
# =============================================================================
df = pd.read_csv('filtered_data.csv')

# clean zipcode
addressZip = df['addr_zip']
addressZip = addressZip.astype(str)
addressZip = addressZip.apply(convertZip)
df['addr_zip'] = addressZip

# get latitude and longitude of each address
# clean address column
address = df['addr_str']
df['addr_str'] = address.astype(str)

locator = Nominatim(user_agent="myGeocoder")
searchEngine= SearchEngine(simple_zipcode=True)

# save (latitude, longitude)
geoLocations = [0 for i in range(df.shape[0])]
for i in range(3577, df.shape[0]):
    street = df['addr_str'][i]
    zipCode = df['addr_zip'][i]
    print('Finding ',i,'th location')
    if not zipCode or zipCode == '':
        geoLocations[i] = (None, None)
    else:
        geoLocations[i] = findLatitude_Longitude(street, zipCode, 'MA','United States', locator, searchEngine)

# =============================================================================
# Google Places API Find nearby places
# =============================================================================

api_key = '' #You'll need your own API key: https://developers.google.com/places/web-service/get-api-key
business_types = ['bus_station','subway_station', 'train_station','airport']

total_results = []
def get_nearby_places(lat, long, business_type, next_page, radius=1609):
    URL = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
		+lat+','+long+'&radius='+str(radius)+'&key='+ api_key +'&type='
		+business_type+'&pagetoken='+next_page)
    r = requests.get(URL)
    response = r.text
    python_object = json.loads(response)
    results = python_object["results"]
    for result in results:
        place_name = result['name']
        place_id = result['place_id']
        geometry = result['geometry']
        location = geometry['location']
        lat_i = location['lat']
        lng_i = location['lng']
        print([business_type, place_name,lat_i,lng_i])
        total_results.append([place_id, business_type, place_name, lat_i, lng_i])
    try:
        next_page_token = python_object["next_page_token"]
    except KeyError:
		#no next page
        return
    time.sleep(1)
    get_nearby_places(lat,long, business_type, next_page_token, radius)

# Tests
get_nearby_places('42.1417653', '-71.2494985', 'train_station', '')

nearByBusStops = [-1 for i in range(len(geoLocations))]
nearBySubwayStops = [-1 for i in range(len(geoLocations))]
nearByTrainStops = [-1 for i in range(len(geoLocations))]

# get number of nearby bus stops within 1 mile
for i in range(len(geoLocations)):
    lat = str(geoLocations[i][0])
    long = str(geoLocations[i][1])
    total_results = []
    print('Finding ',i,'th stops')
    if lat != '' and long != '':
        get_nearby_places(lat, long, business_types[2],'')
        # get number of nearby bus stops for ith location 
        nearByTrainStops[i] = len(total_results)

# =============================================================================
# find average distance to bus, subway, train stops
# =============================================================================
avg_distance = []
# calculate average distance to different stations within 25 miles
def get_avg_distance(lat, long, business_type, next_page, radius=40233):
    URL = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
		+lat+','+long+'&radius='+str(radius)+'&key='+ api_key +'&type='
		+business_type+'&pagetoken='+next_page)
    r = requests.get(URL)
    response = r.text
    python_object = json.loads(response)
    results = python_object["results"]
    for result in results:
        #place_name = result['name']
        #place_id = result['place_id']
        geometry = result.get('geometry')
        location = geometry.get('location')
        lat_i = float(location.get('lat'))
        lng_i = float(location.get('lng'))
        #print([business_type, place_name,lat_i,lng_i])
        distance = calculateDistance(float(lat), float(long), lat_i, lng_i)
        if distance >0:
            avg_distance.append(distance)
    try:
        next_page_token = python_object["next_page_token"]
    except KeyError:
		#no next page
        return
    time.sleep(1)
    get_avg_distance(lat,long, business_type, next_page_token, radius)
# Tests
get_avg_distance('42.1417653', '-71.2494985', 'train_station', '')

avgDistanceBusStops = [-1 for i in range(len(geoLocations))]
numBusStops_25 = [-1 for i in range(len(geoLocations))]
avgDistanceSubwayStops = [-1 for i in range(len(geoLocations))]
numSubwayStops_25 = [-1 for i in range(len(geoLocations))]
avgDistanceTrainStops = [-1 for i in range(len(geoLocations))]
numTrainStops_25 = [-1 for i in range(len(geoLocations))]

# get number of nearby bus stops within 25 miles
for i in range(4467, len(geoLocations)):
    lat = str(geoLocations[i][0])
    long = str(geoLocations[i][1])
    avg_distance = []
    print('Finding',i,'th stops')
    if lat != 'None' and long != 'None':
        get_avg_distance(lat, long, business_types[0],'')
        print('Found', len(avg_distance), 'number of',business_types[0])
        # *** add number of nearby stations into the list***
        numBusStops_25[i] = len(avg_distance)
        # get avg distance of xxx stops for ith location 
        if len(avg_distance) >0:
            avgDistanceBusStops[i] = sum(avg_distance)/len(avg_distance)
        else:
            avgDistanceBusStops[i] = 0
    else:
        print(i,'th Location info not available!')
        
# =============================================================================
# Append locations, with nearby stops on the final dataframe
# =============================================================================
df['latitude'] = [geoLocations[i][0] for i in range(len(geoLocations))]
df['longitutde'] = [geoLocations[i][1] for i in range(len(geoLocations))]
df['nearByBusStops'] = nearByBusStops
df['nearBySubwayStops'] = nearBySubwayStops
df['nearByTrainStops'] = nearByTrainStops

# =============================================================================
# Append avg distance to stations within 30 miles on the final dataframe
# =============================================================================

# read subway and train results from filtered_data_2 and filtered_data_2
df2 = pd.read_csv('filtered_data_2.csv')
df3 = pd.read_csv('filtered_data_3.csv')
df['avgDistanceBusStops'] = avgDistanceBusStops
df['numBusStops_25'] = numBusStops_25

# =============================================================================
# Subway stations
# =============================================================================
avgDistanceSubwayStops = df2['avgDistanceSubwayStops'].to_list()
numSubwayStops_25 = df2['numSubwayStops_25'].to_list()
for i in range(len(geoLocations)):
    if geoLocations[i][0] == None or geoLocations[i][1] == None:
        avgDistanceSubwayStops[i] = -1
        numSubwayStops_25[i] = -1
df['avgDistanceSubwayStops'] = avgDistanceSubwayStops
df['numSubwayStops_25'] = numSubwayStops_25
# =============================================================================
# Train stations
# =============================================================================

avgDistanceTrainStops = df3['avgDistanceTrainStops'].to_list()
numTrainStops_25 = df3['numTrainStops_25'].to_list()
for i in range(len(geoLocations)):
    if geoLocations[i][0] == None or geoLocations[i][1] == None:
        avgDistanceTrainStops[i] = -1
        numTrainStops_25[i] = -1
df['avgDistanceTrainStops'] = avgDistanceTrainStops
df['numTrainStops_25'] = numTrainStops_25

# save final result as csv
df.to_csv('filtered_data_1.csv',index=False)

