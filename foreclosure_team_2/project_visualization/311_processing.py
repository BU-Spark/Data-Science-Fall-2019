import folium
from folium.plugins import HeatMap
import pandas as pd
import matplotlib.pyplot as plt

def data_processing(filename):
    processed_data = []
    df = pd.read_csv(filename)
    df1 = df[['open_dt', 'reason', 'latitude', 'longitude']]
    df1.open_dt = df1.open_dt.str.slice(0,4)
    for i in range(9):
        df_i= df1.loc[df1['open_dt'] == str(2011+i)]
        processed_data.append(df_i)
    return processed_data

processed_data = data_processing('311.csv')

def generateBaseMap(default_location = [42.3601, -71.0589], default_zoom_start=11):
    base_map = folium .Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
    return base_map


def draw_heat_map(data, i):
    base_map = generateBaseMap()
    HeatMap(data=data[['latitude', 'longitude']], radius=8, max_zoom=13).add_to(base_map)
    base_map.save('311_heat_map/311_heat_map_{}.html'.format(i+2011))

# for i in range(9):
#     draw_heat_map(processed_data[i], i)

df = pd.read_csv('311.csv')
fg = plt.figure()
print(df['neighborhood'].value_counts())
pd.value_counts(df['neighborhood']).plot.bar()
fg.autofmt_xdate()
plt.show()