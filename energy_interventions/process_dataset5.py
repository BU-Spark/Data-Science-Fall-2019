import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from folium import folium
from folium.plugins import HeatMap
import folium.folium

abslote_path = os.path.abspath('.')

dataset1_file = abslote_path + "/6ddcd912-32a0-43df-9908-63574f8c7e77.csv"
dataset2_file = abslote_path + "/fy19fullpropassess.csv"
url = abslote_path + '/bzp.geojson'
bzp = f'{url}'
pd.set_option('max_rows', None)

# Clean data
def process_intervention_data_from_file(dataset_file=dataset1_file):
    # filter the column
    raw_data = pd.read_csv(dataset_file)
    raw_data[['parcel_id', 'lat', 'long', 'zip']] = raw_data[['parcel_id', 'lat', 'long', 'zip']].replace({' ': np.nan})
    raw_data = raw_data.dropna()
    # drop duplicated values
    raw_data['parcel_id'] = raw_data['parcel_id'].astype('int64')
    raw_data['zip'] = raw_data['zip'].apply(lambda x: int(x))
    raw_data = raw_data.groupby(['parcel_id']).mean()
    raw_data.reset_index(level=0, inplace=True)
    raw_data['zip'] = raw_data['zip'].apply(lambda x: int(x))
    # raw_data = raw_data[(raw_data['zip'] < 2171) & (raw_data['zip'] > 2108)]
    raw_data['zip'] = raw_data['zip'].apply(lambda x: str(x))
    return raw_data

# Clean data
def process_house_data_from_file(dataset_file=dataset2_file):
    # filte the column
    raw_data = pd.read_csv(dataset_file)[['PID', 'AV_TOTAL']]
    # rename the PID as parcel_id
    raw_data = raw_data.rename(columns={'PID': 'parcel_id'})
    raw_data[['AV_TOTAL']] = raw_data[['AV_TOTAL']].replace({0: np.nan})
    raw_data = raw_data.dropna()
    raw_data['parcel_id'] = raw_data['parcel_id'].astype('int64')
    # drop duplicated values
    raw_data = raw_data.groupby(['parcel_id']).mean()
    raw_data.reset_index(level=0, inplace=True)
    return raw_data

# Calculate the average AV_TOTAL of an area based on zip code
def calculate_average(dataset):
    group = dataset.groupby(['zip']).mean()
    group.reset_index(level=0, inplace=True)
    group = group.rename(columns={'AV_TOTAL': 'average_price'})
    print(group.head())
    return group[['zip', 'average_price']]


def generateBaseMap(default_location=[42.37909, -71.03215]):
    base_map = folium.Map(location=default_location )
    return base_map

# Generate a heat map based on the latitude and longitude, the result is not
# clear, so try to use choropleth map
def draw_heat_map(dataset):
    base_map = generateBaseMap()
    HeatMap(data=dataset[['lat', 'long', 'AV_TOTAL']].
    groupby(['lat', 'long']).mean().
        reset_index().values.tolist(), radius = 8, max_zoom
    = 13).add_to(base_map)
    base_map.save('heatmap.html')

# Draw a scatter picture on a map to figure out whether the area is strictly cut
# based on zip code
def draw_scatter_on_map(data_set):
    color = ['red', 'yellow', 'blue', 'green', 'skyblue', 'purple']
    incidents = folium.map.FeatureGroup()
    for lat, lng, zipcode in zip(data_set['lat'], data_set['long'], data_set['zip']):
        incidents.add_child(
            folium.CircleMarker(
                [lat, lng],
                radius=2,  # define how big you want the circle markers to be
                fill=True,
                fill_color=color[int(zipcode % 5)],
                color=color[int(zipcode % 5)],
                fill_opacity=0.4
            )
        )
    B_map = generateBaseMap()
    B_map.add_child(incidents)
    B_map.save('scatter.html')


def draw_choropleth_map(dataset):
    # Draw the choropleth map according to the average price of AV_TOTAL based on zip code
    m = folium.Map(location=[42.37909, -71.03215], zoom_start=12)
    bins = list(dataset['average_price'].quantile([0, 0.25, 0.5, 0.75, 1]))
    print(dataset.info())
    dataset = dataset.dropna()
    folium.Choropleth(
        geo_data=bzp,
        data=dataset,
        columns=['zipcode', 'average_price'],
        key_on='feature.properties.ZCTA5CE10',
        # fill_color='red',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        highlight=True,
        bins = bins,
        legend_name='Boston Average House Price'
    ).add_to(m)
    m.save('choropleth.html')

intervention_data = process_intervention_data_from_file()
house_data = process_house_data_from_file()

new_data = pd.merge(intervention_data, house_data)
new_data = new_data[['parcel_id', 'AV_TOTAL', 'lat', 'long', 'zip']]
average_price = calculate_average(new_data)
zipcode = average_price['zip'].apply(lambda x: '0' + x)
average_price['zipcode'] = zipcode
average_price['average_price'] = average_price['average_price'].apply(lambda x:int(x))
df1 = pd.merge(new_data, average_price, how='inner')

draw_heat_map(df1)
draw_scatter_on_map(df1)

draw_choropleth_map(average_price)
