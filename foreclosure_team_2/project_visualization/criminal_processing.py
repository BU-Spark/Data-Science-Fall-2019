import folium
from folium.plugins import HeatMap
import pandas as pd
def data_processing(filename):
    processed_data = []
    df = pd.read_csv(filename)
    df1 = df[['YEAR', 'Lat', 'Long']].dropna(subset=['Lat', 'Long'])
    for i in range(5):
        df_i= df1.loc[df1['YEAR'] == 2015+i]
        processed_data.append(df_i)
    return processed_data

processed_data = data_processing('criminal.csv')

def generateBaseMap(default_location = [42.3601, -71.0589], default_zoom_start=11):
    base_map = folium .Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
    return base_map

def draw_heat_map(data, i):
    base_map = generateBaseMap()
    HeatMap(data=data[['Lat', 'Long']], radius=8, max_zoom=13, min_opacity = 0.1, max_val=30).add_to(base_map)
    base_map.save('criminal_heat_map/criminal_heat_map_{}.html'.format(i+2015))

def draw_map(data, i):
    base_map = generateBaseMap()
    for index, row in data.iterrows():
        folium.CircleMarker(location=[row['Lat'], row['Long']], radius=2).add_to(base_map)
    base_map.save('criminal_heat_map/criminal_map_{}.html'.format(i+2015))
for i in range(5):
    draw_heat_map(processed_data[i], i)
    #draw_map(processed_data[i], i)