import requests

head = 'https://services1.arcgis.com/ceiitspzDAHrdGO1/arcgis/rest/services/PATI_Bus_Stops_gdb_(1)/FeatureServer/0/query?where='
target = 'HastusId=15660'
info = '*'
requestMesg = head + target + '&outFields=' + info + '&outSR=4326&f=json'
response = requests.get(requestMesg)
bustop = response.json()
bus_attributes = bustop['features'][0]['attributes']
bus_geometry = bustop['features'][0]['geometry']
print(bus_geometry)