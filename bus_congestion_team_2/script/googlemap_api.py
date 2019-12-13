import googlemaps
import pandas as pd
from datetime import datetime

f = open('../csv/GoogleAPIKey.txt', 'r')
API_key = f.readline()
f.close()

gmaps = googlemaps.Client(key=API_key)


def get_location(location):
    geocode_result = gmaps.geocode(location)
    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitude = geocode_result[0]["geometry"]["location"]["lng"]
    return latitude, longitude


def get_direction(start, end, time=datetime.now()):
    # Request directions via public transit
    directions_result = gmaps.directions(start, end, mode="transit", departure_time=time)
    return directions_result


def generate_locations(filename):
    df = pd.read_csv(filename, low_memory=False)
    df = df.dropna()  # drop samples with NA

    df_area = df.loc[:, "area"]
    location = [get_location(area) for area in df_area]
    df["location"] = location

    df.to_csv("../csv/schools_locations.csv")

# generate_locations("../csv/schools_hr_fixed.csv")
